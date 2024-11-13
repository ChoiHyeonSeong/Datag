"use server";
import { refreshAccessToken } from "@/app/actions/auth";
import { cookies } from "next/headers";

// 상수 정의 - 에러메세지 DEFAULT
const ERROR_MESSAGES = {
  CACHE_CONFLICT: "cache와 next 옵션은 동시에 사용할 수 없습니다.",
  NO_BASE_URL: "BASE_URL이 설정되지 않았습니다.",
  NON_JSON_RESPONSE: "서버가 JSON이 아닌 응답을 반환했습니다.",
  LOGIN_REQUIRED: "로그인이 필요합니다.",
  SERVER_ERROR: "서버에서 오류가 발생했습니다.",
  UNKNOWN_ERROR: "알 수 없는 오류가 발생했습니다.",
} as const;

// 리턴 타입 정의
export type DefaultResponseType<T> = {
  status: number;
  data?: T;
  error?: string;
};

// Fetch 옵션 정의
interface AuthFetchProps {
  BASE_URL?: string; // 기본 도메인 URL, 없을 시 process.env.NEXT_PUBLIC_BACKEND_URL 사용
  endpoint: string; // 요청할 엔드포인트
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH"; // 요청 메소드
  cache?: "no-store" | "force-cache" | null; // 캐시 정책 1
  next?: NextFetchRequestConfig; // 캐시 정책 2
  body?: BodyInit; // 요청 바디
  searchParams?: URLSearchParams | null; // 쿼리스트링
  ContentType?: // Content-Type
  | "application/json"
    | "application/x-www-form-urlencoded"
    | "multipart/form-data";
}

// Fetch 함수
// T: 응답 데이터 타입 제네릭

// JSON 응답 체크 유틸리티 함수
const isJsonResponse = (response: Response): boolean => {
  const contentType = response.headers.get("content-type");
  return contentType?.includes("application/json") ?? false;
};

export async function customFetch<T>({
  BASE_URL,
  endpoint,
  method,
  searchParams,
  cache = "no-store",
  next,
  body,
  ContentType = "application/json",
}: AuthFetchProps): Promise<DefaultResponseType<T>> {
  try {
    // Cache 옵션 검증
    if (cache && next) {
      return {
        status: 400,
        error: ERROR_MESSAGES.CACHE_CONFLICT,
      };
    }

    // console.log(process.env.NEXT_PUBLIC_BACKEND_URL)
    // console.log(BASE_URL)

    // 기본 도메인 URL 설정 - BASE_URL이 없을 시 process.env.NEXT_PUBLIC_BACKEND_URL 사용
    // BASE_URL이나 process.env.NEXT_PUBLIC_BACKEND_URL이 없을 시 에러 발생
    const baseUrl = BASE_URL || process.env.NEXT_PUBLIC_BACKEND_URL;
    if (!baseUrl) {
      throw new Error("BASE_URL이 설정되지 않았습니다.");
    }

    const makeRequest = async (accessToken?: string) => {
      const headers: HeadersInit = {
        "Content-Type": ContentType,
      };
      if (accessToken) {
        headers["Authorization"] = `bearer ${accessToken}`;
      }
      // Fetch 옵션 설정
      const fetchOptions: RequestInit = {};
      if (cache) {
        fetchOptions.cache = cache;
      } else if (next) {
        fetchOptions.next = next;
      }

      // 요청 URL 설정
      const url = new URL(`${baseUrl}${endpoint}`);
      if (searchParams) {
        url.search = searchParams.toString();
      }
      const response = await fetch(url.toString(), {
        ...fetchOptions,
        method,
        headers,
        body,
      });

      // JSON 응답 확인
      if (!isJsonResponse(response)) {
        throw new Error(ERROR_MESSAGES.NON_JSON_RESPONSE);
      }

      return response;
    };

    // Token 가져오기
    const cookieStore = cookies();
    const accessToken = cookieStore.get("accessToken");
    const refreshToken = cookieStore.get("refreshToken");

    let response = await makeRequest(accessToken?.value);

    if (response.status === 401 && refreshToken) {
      const refreshResponse = await refreshAccessToken();
      if (refreshResponse) {
        const retryResult = await makeRequest(refreshResponse);
        response = retryResult;
      } else {
        cookieStore.delete("accessToken");
        cookieStore.delete("refreshToken");
        return {
          status: 401,
          error: ERROR_MESSAGES.LOGIN_REQUIRED,
        };
      }
    }

    const responseData = await response.json();

    if (!response.ok) {
      return {
        status: response.status,
        error: responseData.detail || ERROR_MESSAGES.SERVER_ERROR,
      };
    } else {
      return {
        status: response.status,
        data: responseData as T,
      };
    }
  } catch (error) {
    console.error(error);
    return {
      status: 500,
      error:
        error instanceof Error ? error.message : ERROR_MESSAGES.UNKNOWN_ERROR,
    };
  }
}