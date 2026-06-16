import { Link } from "react-router-dom";

export const Sidebar = () => {

  return (

    <aside className="sidebar">

      <h2>State Machine</h2>

      <nav>

        <ul>

          <li>
            <Link to="/orders">
              Orders
            </Link>
          </li>

          <li>
            <Link to="/tickets">
              Tickets
            </Link>
          </li>
          <li>
            <Link to="/events">
              Events
            </Link>
          </li>
        </ul>

      </nav>

    </aside>

  );
};