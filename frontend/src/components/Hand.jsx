import CardContainer from "../components/CardContainer";

export default function Hand({ cards, dragHandler, type, accept }) {
  return (
    <div className="flex flex-row justify-center">
      {cards.map((c, idx) => {
        return (
          <CardContainer 
            key={`hand-${idx}`}
            cards={c} 
            index={idx} 
            dragHandler={dragHandler}
            type={type}
            accept={accept}
          />
        );
      })}
    </div>
  );
}
