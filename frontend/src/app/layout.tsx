import type { Metadata } from "next";
import { Josefin_Sans as DefaultFont } from "next/font/google";
import "./globals.css";
import DefaultNavbar from "@/components/navbar/DefaultNavbar";
import DefaultFooter from "@/components/footer/DefaultFooter";

const defaultFont = DefaultFont({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "AudioNimbus",
  description: "Convert Audio to AI Generated Images",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`mx-auto flex min-h-screen flex-col justify-between ${defaultFont.className}`}>
        <DefaultNavbar />
        <main className="mx-auto mb-auto flex w-full flex-col gap-4 overflow-y-auto p-2">{children}</main>
        <DefaultFooter />
      </body>
    </html>
  );
}
