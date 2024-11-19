import "./globals.css";
import localFont from "next/font/local";
import { ThemeProvider } from "next-themes";
import Sidebar from "@/components/common/sidebar";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";
import { UserStoreReduxProvider } from "@/components/common/redux-provider";

const pretendard = localFont({
  src: "./fonts/PretendardVariable.woff2",
  display: "swap",
  weight: "45 920",
  variable: "--font-pretendard",
});

const BMJUA = localFont({
  src: "./fonts/BMJUA.woff",
  display: "swap",
  weight: "400",
  variable: "--font-bmjua",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactElement;
}>) {
  return (
    <html
      suppressHydrationWarning
      lang="en"
      className={` ${pretendard.variable} ${BMJUA.variable}`}
    >
      <body id="root">
        <ThemeProvider attribute="class">
          <UserStoreReduxProvider>
            <div className="min-h-screen min-w-screen flex bg-gray-50 dark:bg-gray-900">
              <Sidebar />
              <main className="flex-1">
                <div>{children}</div>
              </main>
            </div>

            <ToastContainer />
          </UserStoreReduxProvider>
        </ThemeProvider>

        <div id="modal-root"></div>
      </body>
    </html>
  );
}
