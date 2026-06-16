import type { Transition }
  from "../../models/transition.ts";

interface Props {
  transitions: Transition[];
}

export const TransitionDiagram = ({
  transitions
}: Props) => {

  return (

    <div>

      <h3>
        State Flow
      </h3>

      {transitions.map(
        (
          transition,
          index
        ) => (

        <div key={index}>

          <div>
            State:
            <strong>
              {" "}
              {transition.new_state}
            </strong>
          </div>

          <div>
            Event:
            {transition.event}
          </div>

          {index !==
            transitions.length - 1
          && <div>↓</div>}

        </div>

      ))}

    </div>

  );
};