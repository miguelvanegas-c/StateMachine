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
        </ul>

      </nav>

    </aside>

  );
};