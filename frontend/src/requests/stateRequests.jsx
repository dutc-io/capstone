import { API } from "../index";


export const FetchState = (gid) => {
  console.log("Fetching state for game ", gid)

  const response = fetch(`${API}/v1/game/${gid}/state/`, {
    method: "GET",
  }).then((res) => res.json());

  return response;
};
