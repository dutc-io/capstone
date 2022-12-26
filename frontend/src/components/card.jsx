
export default function Card({ suit, rank }) {

  const suits = {
    Diamond: "♦",
    Club: "♣",
    Heart: "♥",
    Spade: "♠",
  };

  const ranks = {
    Two: "2",
    Three: "3",
    Four: "4",
    Five: "5",
    Six: "6",
    Seven: "7",
    Eight: "8",
    Nine: "9",
    Ten: "10",
    Jack: "J",
    Queen: "Q",
    King: "K",
    Ace: "A",
  };

  const color = (suit === "Diamond" || suit === "Heard") ? "text-red-600" : "text-black-600"

  return (
    <div className="bg-white mx-2 grid grid-cols-1 border border-grey-800 w-20 h-28">
      <div className={`self-start text-left pl-2 pt-2 text-xl ${color}`}>{ranks[rank]}{suits[suit]}</div>
      <div className={`self-center text-center text-3xl ${color}`}>{suits[suit]}</div>
      <div className={`self-end text-right pr-2 pb-2 text-xl ${color}`}>{ranks[rank]}{suits[suit]}</div>
    </div>
  );
}
