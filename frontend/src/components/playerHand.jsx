import Card from "./card";

export default function PlayerHand() {
  return (
    <div className="flex flex-row justify-center">
      <Card suit="Spade" rank="Queen" />
      <Card suit="Diamond" rank="Four" />
      <Card suit="Club" rank="Eight" />
      <Card suit="Heart" rank="Ace" />
    </div>
  );
}
