import { Link } from "react-router-dom";

export default function Nav() {
  return (
      <nav className="">
        <Link to="/" className="inline-block text-3xl font-medium text-gray-700 hover:text-teal-500 mr-10">&lt; &gt;</Link>
        <Link to="/game" className="inline-block font-medium text-lg text-gray-700 hover:text-teal-500 p-4 pt-5">Play</Link>
        <Link to="/about" className="inline-block font-medium text-lg text-gray-700 hover:text-teal-500 p-4 pt-5">About</Link>
        <Link to="/rules" className="inline-block font-medium text-lg text-gray-700 hover:text-teal-500 p-4 pt-5">Rules</Link>
      </nav>
  );
}
