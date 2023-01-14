import React from "react";
import { createRoot } from "react-dom/client";

import { createBrowserRouter, RouterProvider } from "react-router-dom";

import ErrorPage from "./pages/errorPage";
import IndexPage from "./pages/indexPage";
import GameIndexPage from "./pages/game/gameIndexPage";
import AboutPage from "./pages/aboutPage";
// import GamePlayPage from "./pages/game/gamePlayPage";
import GamePlayPage from "./pages/game/gamePlayPage";
import RulePage from "./pages/rulePage";

import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <GameIndexPage />,
      },
      {
        path: "/game",
        element: <GamePlayPage />,
      },
      {
        path: "/about",
        element: <AboutPage />,
      },
      {
        path: "/rules",
        element: <RulePage />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
