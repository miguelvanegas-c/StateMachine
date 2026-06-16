interface Props {
  children: React.ReactNode;
}

export const Modal = ({
  children
}: Props) => {

  return (

    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,

        backgroundColor:
          "rgba(0,0,0,0.4)",

        display: "flex",

        justifyContent:
          "center",

        alignItems:
          "center"
      }}
    >

      <div
        style={{
          background: "white",
          padding: "20px",
          minWidth: "600px"
        }}
      >
        {children}
      </div>

    </div>

  );
};