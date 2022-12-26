import PlayerHand from "../../components/playerHand";
import TableHand from "../../components/tableHand";

export default function GamePlayPage() {
  return (

      <div className="grow justify-center">
        <section className="grid grid-rows-3 min-h-full">
    
          {/* Other Players */}
          <div className="text-center self-start pt-14">
              <span className="text-slate-500">Player Name</span>&nbsp;•&nbsp; 
              <span className="font-medium text-lg text-slate-800">▷ Player Name ◁</span>&nbsp;•&nbsp;
              <span className="text-slate-500">Player Name</span> 
          </div>

          {/* Table Cards */}
          <div className="text-center self-center align-middle">
            <TableHand />
          </div>

          {/* Player Cards */}
          <div className="text-center self-end">
            <PlayerHand /> 
          </div>
        </section>
      </div>
  );
}

