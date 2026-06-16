interface MetadataField {
  key: string;
  value: string;
}

interface Props {
  metadataFields: MetadataField[];

  onAdd: () => void;

  onRemove: (
    index: number
  ) => void;

  onUpdate: (
    index: number,
    field: "key" | "value",
    value: string
  ) => void;
}

export const MetadataFields = ({
  metadataFields,
  onAdd,
  onRemove,
  onUpdate
}: Props) => {

  return (

    <div>

      <h3>Metadata</h3>

      {metadataFields.map(
        (field, index) => (

        <div
          key={index}
          style={{
            display: "flex",
            gap: "10px",
            marginBottom: "10px"
          }}
        >

          <input
            placeholder="Key"

            value={field.key}

            onChange={(e) =>
              onUpdate(
                index,
                "key",
                e.target.value
              )
            }
          />

          <input
            placeholder="Value"

            value={field.value}

            onChange={(e) =>
              onUpdate(
                index,
                "value",
                e.target.value
              )
            }
          />

          <button
            onClick={() =>
              onRemove(index)
            }
          >
            Remove
          </button>

        </div>

      ))}

      <button onClick={onAdd}>
        + Add field
      </button>

    </div>
  );
};