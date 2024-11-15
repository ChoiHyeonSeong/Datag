"use server";

import { cookies } from "next/headers";

import { LoginResponseType, RefreshResponseType } from "@/types/auth";
import {
  accessTokenDuration,
  refreshTokenDuration,
} from "@/lib/constants/token-duration";
import { DefaultResponseType } from "@/types/default";

export const check_auth = async (formData: FormData) => {
  console.log("check_auth");
  const email = formData.get("email");
  const password = formData.get("password");
  if (!email || !password) {
    return {
      status: 400,
      error: "Email and password are required",
    };
  }
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
        cache: "no-store",
      }
    );

    if (!response || !response.ok || response.status >= 400) {
      console.log("login fail here ---- ");
      console.log(response);
      return {
        error: "유효하지 않는 이메일 또는 비밀번호입니다.",
        status: 401,
      };
    }

    const data: DefaultResponseType<LoginResponseType> = await response.json();

    if (!data?.data || !data.data.access_token) {
      console.log("login fail");
      return {
        error: "Invalid",
        status: 400,
      };
    }

    console.log("login success = ", data.data?.access_token);
    const cookieStore = await cookies();

    cookieStore.set({
      name: "refreshToken",
      value: data.data.refresh_token,
      httpOnly: true,
      path: process.env.NEXT_PUBLIC_FRONTEND_URL,
      maxAge: refreshTokenDuration,
    });

    cookieStore.set({
      name: "accessToken",
      value: data.data.access_token,
      httpOnly: true,
      path: process.env.NEXT_PUBLIC_FRONTEND_URL,
      maxAge: accessTokenDuration,
    });

    console.log();

    return {
      status: response.status,
      data: {
        UserData: data.data.user,
      },
    };
  } catch (error) {
    console.error("Login failed:", error);
    return {
      error: "Something went wrong",
      status: 500,
    };
  }
};

// 쿠키에 담긴 accessToken을 이용하여 사용자의 인증 상태를 확인
// accessToken이 유효하면 true, 그렇지 않으면 false를 반환 (없는 경우도 고려)
export const verifyAccessToken = async (accessToken: string) => {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/profile`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        cache: "no-store",
      }
    );
    if (!response.ok) {
      return false;
    }
    return true;
  } catch (error) {
    console.error("Token verification failed:", error);
    return false;
  }
};

// 쿠키에 담긴 refreshToken을 이용하여 새로운 accessToken을 발급
// 새로운 accessToken을 반환하며, refreshToken이 유효하지 않은 경우 null을 반환
// refreshToken이 유효하지 않은 경우, 쿠키에서 refreshToken과 accessToken을 삭제
// 새로운 accessToken을 발급받은 경우, 쿠키에 새로운 accessToken과 refreshToken을 저장
export const refreshAccessToken = async (): Promise<string | null> => {
  const cookieStore = cookies();
  const refreshToken = cookieStore.get("refreshToken");
  if (!refreshToken) return null;
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/refresh`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${refreshToken.value}`,
        },
      }
    );

    if (!response.ok) {
      cookieStore.delete("refreshToken");
      cookieStore.delete("accessToken");
      return null;
    }

    const data: RefreshResponseType = await response.json();

    cookieStore.set({
      name: "accessToken",
      value: data.access_token,
      httpOnly: true,
      maxAge: accessTokenDuration,
    });
    cookieStore.set({
      name: "refreshToken",
      value: data.refresh_token,
      httpOnly: true,
      maxAge: refreshTokenDuration,
    });
    return data.access_token;
  } catch (error) {
    console.error("Token refresh failed:", error);
    cookieStore.delete("refreshToken");
    cookieStore.delete("accessToken");
    return null;
  }
};

export const logout = async () => {
  try {
    await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });
  } catch (error) {
    console.error("Logout failed:", error);
  } finally {
    cookies().delete("refreshToken");
    cookies().delete("accessToken");
    return null;
  }
};

export const getAccessToken = async () => {
  const cookieStore = cookies();
  const accessToken = cookieStore.get("accessToken");
  const refreshToken = cookieStore.get("refreshToken");

  if (accessToken) {
    return accessToken.value;
  } else {
    if (refreshToken) {
      const result = await refreshAccessToken();
      return result;
    } else {
      return null;
    }
  }
};