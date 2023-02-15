import { API } from "../index";


export const FetchState = (gid) => {
  console.log("Fetching state for game ", gid)

  const response = fetch(`${API}/v1/state/`, {
    method: "POST",
    body: JSON.stringify({ game: gid, }),
  }).then((res) => res.json());

  return response;
};
