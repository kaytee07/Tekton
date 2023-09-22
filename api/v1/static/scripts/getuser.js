const trash = document.querySelector('svg.trash');
const edit = document.querySelector('svg.edit');
const user = document.querySelector('div.student_details');

trash.addEventListener('click', () => {
    deleteuser(user.id)
})


function deleteuser(id) {
const url = `http://localhost:5001/api/v1/deleteuser/${id}`;
console.log(url)
const requestOptions = {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
};

fetch(url, requestOptions)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((responseData) => {
      console.log('works')
  })
  .catch((error) => {
    console.error("Fetch error:", error);
  });    
}

function edituser() {
    
}
