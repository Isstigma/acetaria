import Dropdown from "../components/DropDownBtn"


export default function Runs(){
  return (
    <div>
    {/* category selections */}
      <div className="my-8 flex justify-between items-center h-31.5 w-full bg-bg-dark rounded-3xl px-6">

        <div className="grid grid-cols-2 gap-2 h-24 w-90 ">
            <button className="bg-bg-light rounded-2xl p-2 h-10">Memmory of Chaos</button>
            <button className="bg-bg-light rounded-2xl p-2 h-10">Pure Fiction</button>
            <button className="bg-bg-light rounded-2xl p-2 h-10">Appocalyptic shadow</button>
            <button className="bg-bg-light rounded-2xl p-2 h-10 ">Anomaly Arbitration</button>
        </div>

        <div className="flex justify-center items-center gap-3 ">
          <Dropdown
        label="Season & Boss"
        items={[
          "Memory of Chaos",
          "Pure Fiction",
          "Apocalyptic Shadow",
          "Anomaly Arbitration",
        ]}
        width={200}
      />
          <Dropdown
        label="Filter by category"
        items={[
          "0-Cycle",
          "Show all runs",
          "Full stars",
        ]}
        width={150}
      />
      <Dropdown
        label="Cost bracket"
        items={[
          "All costs",
          "0-8",
          "9-18",
          "19-35",
          "36-48",
        ]}
        width={150}
      />
      <Dropdown
        label="Sort Order"
        items={[
          "Score",
          "Cost",
          "Latest",
        ]}
        width={150}
      />

        </div>


      </div>
    
      <div className="my-8 flex justify-between items-center h-16 w-full bg-bg-dark rounded-3xl px-6">
        <div className="flex justify-between items-center gap-3">
            <button className="bg-bg-light rounded-2xl px-4 py-2 w-44">Select characters</button>
            <button className="bg-bg-light rounded-2xl px-4 py-2 w-44">Select Light Cones</button>
        </div>

        <div>

        </div>
      </div>

    </div>
  )
}

