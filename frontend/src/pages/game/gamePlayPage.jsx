import { useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import Hand from "../../components/Hand";

const fakeAPIResponse = {
  table: [
    { suit: "Diamond", rank: "King" },
    { suit: "Diamond", rank: "Queen" },
    { suit: "Club", rank: "Jack" },
    { suit: "Spade", rank: "Two" },
  ],
  player: [
    { suit: "Heart", rank: "Ace" },
    { suit: "Heart", rank: "Ten" },
    { suit: "Spade", rank: "Ace" },
    { suit: "Club", rank: "Five" },
  ],
};

export default function GamePlayPage() {
  const [table, setTable] = useState(fakeAPIResponse.table);
  const [player, setPlayer] = useState(fakeAPIResponse.player);

  const handleDrag = (item, type, moveToidx) => {
    switch (type) {
      case "PLAYER":
        console.log("Player moved");
        let pc = player.splice(item.index, 1)[0];
        setPlayer([...player]);
        table.splice(moveToidx, 0, pc);
        setTable([...table]);
        break;
      case "TABLE":
        console.log("Table moved");
        let tc = table.splice(item.index, 1)[0];
        setTable([...table]);
        player.splice(moveToidx, 0, tc);
        setPlayer([...player]);
        break;
      default:
        console.log("Discard");
        break;
    }
  };

  if (player === null || table === null) {
    return <p>loading</p>;
  }

  return (
    <div className="grow justify-center">
      <section className="grid grid-rows-3 min-h-full">
        <DndProvider backend={HTML5Backend}>
          {/* Other Players */}
          <div className="text-center self-start pt-14">
            <span className="text-slate-500">Player Name</span>&nbsp;•&nbsp;
            <span className="font-medium text-lg text-slate-800">
              ▷ Player Name ◁
            </span>
            &nbsp;•&nbsp;
            <span className="text-slate-500">Player Name</span>
          </div>

          {/* Table Cards */}
          <div className="text-center self-center align-middle">
            <Hand
              cards={table}
              foreman={handleDrag}
              type="TABLE"
              accept="PLAYER"
            />
          </div>

          {/* Player Cards */}
          <div className="text-center self-end">
            <Hand
              cards={player}
              foreman={handleDrag}
              type="PLAYER"
              accept="TABLE"
            />
          </div>
        </DndProvider>
      </section>
    </div>
  );
}
