"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

type SideBarItemType = {
  name: string;
  href: string;
};

const SideBarItemStore: SideBarItemType[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
  },
  {
    name: "About",
    href: "/about",
  },
];

export default function SideBarItems() {
  const pathname = usePathname();

  return (
    <>
      {SideBarItemStore.map((item) => (
        <li
          key={item.name}
          className={`${
            pathname.includes(item.href) ? "text-primary" : "hover:text-base-content"
          } duration-200 hover:scale-[0.98]`}
        >
          <Link href={item.href}>{item.name}</Link>
        </li>
      ))}
    </>
  );
}
