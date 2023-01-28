import { Outlet } from "react-router-dom";

import Nav from "../components/nav";
import Footer from "../components/footer";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

export default function IndexPage() {
  return (
    <main className="h-full flex flex-col container mx-auto px-4 sm:px-6 lg:px-8">
      {/* Navigation */}
      <div><Nav /></div>

      {/* Content */}
      <DndProvider backend={HTML5Backend}>
      <Outlet />
      </DndProvider>
      {/* Footer */}
      <div><Footer /></div>
    </main>
  );
}
