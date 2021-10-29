import React, { useState, useEffect } from "react";
import MaterialTable from "material-table";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((response) => response.json())
      .then((result) => {
        setData(result.slice(0, 5));
      });
  }, []);

  const columns = [
    { title: "Name", field: "name" },
    { title: "UserName", field: "username" },
    { title: "Email", field: "email" },
    { title: "Phone", field: "phone" },
    { title: "Website", field: "website" },
  ];

  const addNewRow = (newRow) =>
    new Promise((resolve, reject) => {
      setData([...data, newRow]);
      resolve();
    });

  const deleteRow = (selectedRow) =>
    new Promise((resolve, reject) => {
      const updatedData = [...data];
      updatedData.splice(selectedRow.tableData.id, 1);
      setData(updatedData);
      resolve();
    });

  const updateRow = (newRow, oldRow) =>
    new Promise((resolve, reject) => {
      const updatedData = [...data];
      updatedData[oldRow.tableData.id] = newRow;
      setData(updatedData);
      resolve();
    });

  const showTable = data.length ? (
    <MaterialTable
      title="User data"
      columns={columns}
      data={data}
      options={{
        search: false,
        paging: true,
        pageSizeOptions: [2, 5, 10, 15, 20, 25],
        pageSize: 2,
        addRowPosition: "first",
        actionsColumnIndex: -1,
      }}
      editable={{
        onRowAdd: addNewRow,
        onRowUpdate: updateRow,
        onRowDelete: deleteRow,
      }}
    />
  ) : (
    <p>...loading</p>
  );
  return <div>{showTable}</div>;
};

export default App;
