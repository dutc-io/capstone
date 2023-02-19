import { useDrop } from "react-dnd";
import { useState, useEffect } from "react";

import { useQuery } from "react-query";
import Hand from "../../components/Hand";
import { FetchState } from "../../requests/stateRequests";

const fakeAPIResponse = {
  table: [
    { suit: "Diamond", rank: "King" },
    { suit: "Heart", rank: "King" },
    { suit: "Club", rank: "King" },
    { suit: "Spade", rank: "King" },
  ],
  player: [
    { suit: "Diamond", rank: "Ace" },
    { suit: "Heart", rank: "Ace" },
    { suit: "Club", rank: "Ace" },
    { suit: "Spade", rank: "Ace" },
  ],
};

export default function GamePlayPage() {
  const [apiCall, setApiCall] = useState("");
  const [table, setTable] = useState(fakeAPIResponse.table);
  const [player, setPlayer] = useState(fakeAPIResponse.player);

  const { isLoading, isFetching, error, data } = useQuery({
    queryKey: ["gameState"], // We prob don't want to cache this
    queryFn: () => FetchState(1), // Need game ID
  });
  useEffect(() => {
    if (isFetching) {
      return;
    }
    if (!isFetching && data) {
      const hands = data["hands"];
      const firstPlayer = hands[Object.keys(hands)[0]]

      // TODO: We need to do some transformation of the data here. 
      const _table = data["table"];

      console.log("FP: ", firstPlayer)
      console.log(firstPlayer);
      console.log("table", _table);
      // Set to the player you want, for testing current game using jefro
      setPlayer(firstPlayer);
      setTable(_table);
    }
  }, [isFetching]);

  const addPlayer = (c) => setPlayer([...player, c]);
  const playerPopIndex = (i) => {
    const c = player.splice(i, 1)[0];
    setPlayer([...player]);
    return c;
  };
  const addTable = (c) => setTable([...table, c]);
  const tablePopIndex = (i) => {
    const c = table.splice(i, 1)[0];
    setTable([...table]);
    return c;
  };

  const handleDrag = (item, type, moveToIdx) => {
    console.log("Item: ", item, " Type: ", type, " Move to: ", moveToIdx);
    let c;
    if (type === "PLAYER") {
      // We're building on table's cards
      if (moveToIdx !== "TRAIL") {
        setApiCall(`Building: player ${item.index}, on table  ${moveToIdx}`);
        c = playerPopIndex(item.index);
        if (table[moveToIdx] instanceof Array) {
          table[moveToIdx].push(c);
        } else {
          table[moveToIdx] = [table[moveToIdx], c];
        }
        setTable([...table]);
        return;
      }

      // We're trailing
      setApiCall(`Trialing: player , ${item.index}`);
      c = playerPopIndex(item.index);
      setTable([...table, c]);
    } else if (type === "TABLE") {
      setApiCall(`Capturing: player ${moveToIdx} on table ${item.index}`);
      playerPopIndex(moveToIdx);
      tablePopIndex(item.index);
    }
  };

  const [{ canDrop, isOver }, drop] = useDrop(
    () => ({
      accept: "PLAYER",
      drop: (item, monitor) => {
        const didDrop = monitor.didDrop();
        if (didDrop) {
        } else {
          console.log("Trailing: ", item);
          handleDrag(item, "PLAYER", "TRAIL");
        }
      },
      collect: (monitor) => ({
        isOver: monitor.isOver({ shallow: true }),
        canDrop: monitor.canDrop(),
      }),
    }),
    [table, player]
  );

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>An error has occurred: {error.message}</p>;

  // console.log(data)

  if (player === null || table === null) {
    return <p>loading</p>;
  }

  const isActive = canDrop && isOver;
  let bgColor = "bg-white";
  if (isActive) {
    bgColor = "bg-blue-100";
  } else if (canDrop) {
    bgColor = "bg-blue-50";
  }

  return (
    <div className="grow justify-center">
      <div className="h-full">
        <section
          ref={drop}
          className={`grid grid-rows-3 min-h-full ${bgColor}`}
        >
          <div className="text-center row-span-1 self-start align-middle">
            <strong>API CALL</strong> {apiCall}
          </div>
          <div className="text-center row-span-1 self-center align-middle">
            <Hand
              cards={table}
              dragHandler={handleDrag}
              type="TABLE"
              accept="PLAYER"
            />
          </div>
          <div className="text-center row-span-1 self-end align-middle">
            <Hand
              cards={player}
              dragHandler={handleDrag}
              type="PLAYER"
              accept="TABLE"
            />
          </div>
        </section>
      </div>
    </div>
  );
}
