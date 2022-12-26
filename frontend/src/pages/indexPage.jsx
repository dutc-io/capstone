import { Outlet } from "react-router-dom";

import Nav from "../components/nav";
import Footer from "../components/footer";

export default function IndexPage() {
  return (
    <main className="h-full flex flex-col container mx-auto px-4 sm:px-6 lg:px-8">
      {/* Navigation */}
      <div><Nav /></div>

      {/* Content */}
      <Outlet />

      {/* Footer */}
      <div><Footer /></div>
    </main>
  );
}
