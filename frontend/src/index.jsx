import React from "react";
import { createRoot } from "react-dom/client";

import { QueryClient, QueryClientProvider } from "react-query";

import { createBrowserRouter, RouterProvider } from "react-router-dom";

import ErrorPage from "./pages/errorPage";
import IndexPage from "./pages/indexPage";
import GameIndexPage from "./pages/game/gameIndexPage";
import AboutPage from "./pages/aboutPage";
import GamePlayPage from "./pages/game/gamePlayPage";
import RulePage from "./pages/rulePage";

import "./index.css";

let API = "http://PRODUCTION";
if (import.meta.env.VITE_DEVELOPMENT == "DEV") {
  API = "http://127.0.0.1:8000";
}

const queryClient = new QueryClient();
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
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);

export {API}
