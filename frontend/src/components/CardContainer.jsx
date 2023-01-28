import { useDrag, useDrop } from "react-dnd";
import Card from "../components/card";

export default function CardContainer({
  cards,
  index,
  dragHandler,
  type,
  accept,
}) {
  const cardInfo = { type: type, index: index };
  const [{ opacity }, dragRef] = useDrag(
    () => ({
      type: type,
      item: cardInfo,
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1,
      }),
    }),
    [index, dragHandler, cards, accept, type]
  );
  const [{ canDrop, isOver }, drop] = useDrop(
    () => ({
      accept: accept,
      drop: (item) => {
        dragHandler(item, accept, index);
      },
      collect: (monitor) => ({
        isOver: monitor.isOver({ shallow: true }),
        canDrop: monitor.canDrop(),
      }),
    }),
    [index, dragHandler, cards, accept, type]
  );

  const isActive = canDrop && isOver;
  let bgColor = "bg-white";
  if (isActive) {
    bgColor = "bg-green-200";
  } else if (canDrop) {
    bgColor = "bg-green-50";
  }

  if (cards instanceof Array) {
    return (
      <div ref={drop} className={`inline-block ${bgColor}`}>
        <div ref={dragRef} style={{ opacity }} data-testid={`card`}>
          {cards.map((c) => {
            return (
              <Card
                key={`card-${index}-${c.rank}-${c.suit}`}
                rank={c.rank}
                suit={c.suit}
              />
            );
          })}
        </div>
      </div>
    );
  } else {
    return (
      <div ref={drop} className={`inline-block ${bgColor}`}>
        <div ref={dragRef} style={{ opacity }} data-testid={`card`}>
          <Card
            key={`card-${index}-${cards.rank}-${cards.suit}`}
            rank={cards.rank}
            suit={cards.suit}
          />
        </div>
      </div>
    );
  }
}
