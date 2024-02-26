import { Poppins as FooterFont } from "next/font/google";
import Link from "next/link";

const footerFont = FooterFont({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export default function DefaultFooter() {
  return (
    <footer
      className={`footer footer-center bg-base-200 text-base-content rounded p-10 text-xs ${footerFont.className}`}
    >
      <nav className="grid grid-flow-col gap-4">
        <Link href={"/about"} className="link link-hover">
          About
        </Link>
        <Link href={"/contact"} className="link link-hover">
          Contact
        </Link>
      </nav>
      <aside>
        <p>Copyright © {new Date().getFullYear()} - All right reserved by AudioNimbus Ltd</p>
      </aside>
    </footer>
  );
}
