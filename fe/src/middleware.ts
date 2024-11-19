import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import {
  accessTokenDuration,
  refreshTokenDuration,
} from "./lib/constants/token-duration";
import { DefaultResponseType } from "./types/default";
import { RefreshResponseType } from "./types/auth";
import { verifyAccessToken } from "./app/actions/auth";

const publicRoutes = ["/login", "/signup", "/"];

export async function middleware(request: NextRequest) {
  const refreshTokenCookie = request.cookies.get("refreshToken");
  const accessTokenCookie = request.cookies.get("accessToken");
  const path = request.nextUrl.pathname;
  const isPublicRoute = publicRoutes.includes(path);
  const res = NextResponse.next();

  if (path === "/") {
    return NextResponse.next();
  }

  // refreshToken으로 토큰 갱신 시도 중인지 확인
  const isRefreshing = request.headers.get("x-refreshing-token");

  // 엑세스 토큰 있을 경우
  if (accessTokenCookie) {
    const accessTokenVerify = await verifyAccessToken(accessTokenCookie.value);

    // 유효한 토큰인 경우 - 미들웨어 종료
    if (accessTokenVerify) {
      if (isPublicRoute) {
        return NextResponse.redirect(new URL("/project", request.url));
      }
      return res;
    }
    // 유효하지 않은 토큰인 경우
    else {
      request.cookies.delete("accessToken");
    }
  }

  // refreshToken이 있고 갱신 시도 중이 아닌 경우
  if (refreshTokenCookie && !isRefreshing) {
    try {
      const refreshResponse = NextResponse.next();
      refreshResponse.headers.set("x-refreshing-token", "true");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/refresh`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${refreshTokenCookie.value}`,
          },
        }
      );

      if (!response.ok) {
        // 리프레시 토큰이 유효하지 않은 경우 쿠키 삭제
        console.error("response result", response.status);
        const loginRedirect = NextResponse.redirect(
          new URL("/login", request.url)
        );
        loginRedirect.cookies.delete("accessToken");
        loginRedirect.cookies.delete("refreshToken");
        return loginRedirect;
      }

      const data: DefaultResponseType<RefreshResponseType> =
        await response.json();

      if (!data?.data) {
        const loginRedirect = NextResponse.redirect(
          new URL("/login", request.url)
        );
        loginRedirect.cookies.delete("accessToken");
        loginRedirect.cookies.delete("refreshToken");
        return loginRedirect;
      }

      // 토큰 갱신 성공
      const redirectUrl = isPublicRoute ? "/project" : request.nextUrl.pathname;
      const finalResponse = NextResponse.redirect(
        new URL(redirectUrl, request.url)
      );

      finalResponse.cookies.set({
        name: "accessToken",
        value: data.data.access_token,
        httpOnly: true,
        path: "/",
        maxAge: accessTokenDuration,
      });

      finalResponse.cookies.set({
        name: "refreshToken",
        value: data.data.refresh_token,
        httpOnly: true,
        path: "/",
        maxAge: refreshTokenDuration,
      });

      return finalResponse;
    } catch (error) {
      const loginRedirect = NextResponse.redirect(
        new URL("/login", request.url)
      );
      loginRedirect.cookies.delete("accessToken");
      loginRedirect.cookies.delete("refreshToken");
      return loginRedirect;
    }
  }

  // 토큰이 없는 경우
  if (!isPublicRoute) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return res;
}
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
