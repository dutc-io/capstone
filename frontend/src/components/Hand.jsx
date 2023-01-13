import Card from "../components/card";

export default function Hand({ cards, foreman, type, accept }) {
  return (
    <div className="flex flex-row justify-center">
      {cards.map((c, idx) => {
        // console.log(type, " ", `${c.suit}${c.rank}`, " at ", idx);
        return (
          <Card
            foreman={foreman}
            key={`${c.suit}${c.rank}`}
            suit={c.suit}
            rank={c.rank}
            type={type}
            accept={accept}
            index={idx}
          />
        );
      })}
    </div>
  );
}
