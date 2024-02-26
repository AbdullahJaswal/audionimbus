import SideBarItems from "@/components/sidebar/SideBarItems";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <section>
      <div className="drawer lg:drawer-open">
        <input id="dashboard-sidebar" type="checkbox" className="drawer-toggle" />
        <div className="drawer-content">
          {children}

          <label htmlFor="dashboard-sidebar" className="btn btn-primary drawer-button lg:hidden">
            Open drawer
          </label>
        </div>
        <div className="drawer-side lg:h-min">
          <label htmlFor="dashboard-sidebar" aria-label="close sidebar" className="drawer-overlay"></label>
          <ul className="h-full menu bg-base-100 text-base-content/60 flex w-80 flex-col gap-2 text-base">
            <SideBarItems />
          </ul>
        </div>
      </div>
    </section>
  );
}
