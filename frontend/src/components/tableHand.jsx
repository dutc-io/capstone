import Card from "./card";

export default function TableHand() {
  return (
    <div className="flex flex-row justify-center">

      <div className="mx-1 bg-slate-100 px-1 py-3">
        <Card suit="Heart" rank="Two" />
      </div>

      <div className="mx-1 bg-slate-100 px-1 py-3">
        <Card suit="Club" rank="King" />
      </div>

      <div className="mx-1 bg-slate-100 px-1 py-3">
        <Card suit="Spade" rank="Ten" />
      </div>

      <div className="mx-1 bg-slate-100 px-1 py-3">
        <Card suit="Diamond" rank="Ace" />
      </div>

    </div>
  );
}
