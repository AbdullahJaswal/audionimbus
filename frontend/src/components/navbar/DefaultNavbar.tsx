import Link from "next/link";

export default function DefaultNavbar() {
  return (
    <div className="navbar bg-base-100">
      <Link href={"/"} className="btn btn-ghost text-primary text-xl font-semibold">
        AudioNimbus
      </Link>
    </div>
  );
}
