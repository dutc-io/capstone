import { useDrag, useDrop } from "react-dnd";
export default function Card({ index, foreman, suit, rank, accept, type }) {
  const actor = accept;
  const cardInfo = { type: type, index: index, card: `${suit} ${rank}` };

  const [{ opacity }, dragRef] = useDrag(
    () => ({
      type: type,
      item: cardInfo,
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1,
      }),
    }),
    [index, foreman, suit, rank, accept, type]
  );
  const [{ canDrop, isOver }, drop] = useDrop(
    () => ({
      accept: accept,
      drop: (item) => {
        foreman(item, actor, index);
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
        canDrop: monitor.canDrop(),
      }),
    }),
    [index, foreman, suit, rank, accept, type]
  );

  const isActive = canDrop && isOver;
  let backgroundColor = "bg-blue-50";
  if (isActive) {
    backgroundColor = "bg-green-100";
  } else if (canDrop) {
    backgroundColor = "bg-green-50";
  }
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

  const color =
    suit === "Diamond" || suit === "Heart" ? "text-red-600" : "text-black-600";

  return (
    <div ref={drop} className={`mx-1 px-1 py-3 ${backgroundColor}`}>
      <p>Index: {index}</p>
      <div
        ref={dragRef}
        style={{ opacity }}
        className="bg-white mx-2 grid grid-cols-1 border border-grey-800 rounded w-20 h-28"
        data-testid={`card`}
      >
        <div className={`self-start text-left pl-2 pt-2 text-xl ${color}`}>
          {ranks[rank]}
          {suits[suit]}
        </div>
        <div className={`self-center text-center text-3xl ${color}`}>
          {suits[suit]}
        </div>
        <div className={`self-end text-right pr-2 pb-2 text-xl ${color}`}>
          {ranks[rank]}
          {suits[suit]}
        </div>
      </div>
    </div>
  );
}
