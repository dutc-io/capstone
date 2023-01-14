import { useDrop } from "react-dnd";
import { useState } from "react";

import Hand from "../../components/Hand";
import CardContainer from "../../components/CardContainer";

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

  const addPlayer = (c) => setPlayer([...player, c]);
  const playerPopIndex = (i) => {
    const c = player.splice(i, 1)[0]
    setPlayer([...player])
    return c
  }
  const addTable = (c) => setTable([...table, c]);
  const tablePopIndex = (i) => {
    const c = table.splice(i, 1)[0]
    setTable([...table])
    return c
  }

  const handleDrag = (item, type, moveToIdx) => {
    console.log("Item: ", item, " Type: ", type, " Move to: ", moveToIdx);
    let c;
    if (type === "PLAYER") {
      // We're building on table's cards 
      if (moveToIdx !== "TRAIL"){
        setApiCall(`Building: player ${item.index}, on table  ${moveToIdx}`)
        return
      } 

      // We're trailing 
      // setApiCall(`Trialing: player , ${item.index}`)
      c = playerPopIndex(item.index)
      setTable(c)
    } else if (type === "TABLE") {
      setApiCall(`Capturing: player ${moveToIdx} on table ${item.index}`)
      playerPopIndex(moveToIdx)
      tablePopIndex(item.index)
    }
    // switch (type) {
    //   case "PLAYER":
    //     // Player can either trail or build
    //     if (moveToidx === "") {
    //       setApiCall(`TRAIL: Player trails card index ${item.index}`);
    //       let pc = playerPopIndex(item.index) //player.splice(item.index, 1)[0]
    //       addTable(pc)
    //       setPlayer([...player])
    //       // console.log("Spliced player card: ", pc)
    //       // table.splice(table.length, 0, pc)
    //       // setPlayer([...player])
    //       // setTable([...table])
    //     } else {
    //       setApiCall(
    //         `BUILD: Player card index ${item.index} to Table index: ${moveToidx}`
    //       );
    //       let bpc = player.splice(item.index, 1)[0];
    //       setPlayer([...player]);
    //       // This feels wrong. But also works, so how wrong could it be?
    //       if (table[moveToidx] instanceof Array) {
    //         table[moveToidx].push(bpc);
    //       } else {
    //         table[moveToidx] = [table[moveToidx], bpc];
    //       }
    //       setTable([...table]);
    //     }
    //     break;
    //   case "TABLE":
    //     setApiCall(
    //       `CAPTURE: Table card index ${item.index} captured by Player card index: ${moveToidx}`
    //     );
    //     let tc = table.splice(item.index, 1)[0];
    //     let tpc = player.splice(moveToidx, 1)[0];
    //     setTable([...table]);
    //     setPlayer([...player]);
    //     break;
    //   default:
    //     break;
    // }
  };

  const [{ canDrop, isOver }, drop] = useDrop(
    () => ({
      accept: "PLAYER",
      drop: (item, monitor) => {
        const didDrop = monitor.didDrop()
        if (didDrop) {
        } else {
          console.log("Trailing: ", item)
          handleDrag(item, "PLAYER", "TRAIL");
        }
      },
      collect: (monitor) => ({
        isOver: monitor.isOver({ shallow: true }),
        canDrop: monitor.canDrop(),
      }),
    }),
    []
  );

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
  // console.log(" ") 
  // console.log("Player") 
  // console.log(player)
  // console.log(" ") 
  // console.log("Table ") 
  // console.log(table)
  // console.log(" ") 
  return (
    <div className="grow justify-center">
      <div className="h-full">
        <section
          ref={drop}
          className={`grid grid-rows-3 min-h-full ${bgColor}`}
        >
          <div className="text-center row-span-1 self-start align-middle">
            <strong>API CALL</strong> {apiCall}
            <p>Table length: {table.length}</p>
            <p>{table.map((c) => <><i>{c.rank}</i> {c.suit}, </>)}</p>
            <p>Plyer length: {player.length}</p>
            <p>{player.map((c) => <><i>{c.rank}</i> {c.suit}, </>)}</p>
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
