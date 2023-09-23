const trash = document.querySelectorAll('svg.trash');
const edit = document.querySelector('svg.edit');
const user = document.querySelector('div.student_details');

for (let i = 0; i < trash.length; i++) {
     trash[i].addEventListener("click", function() {
	 console.log(this.parentElement.parentElement.id)
	 deleteuser(this.parentElement.parentElement.id)
     });
 }


function deleteuser(id) {
const url = `http://localhost:5001/api/v1/deletecourse/${id}`;
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
      location.reload()
  })
  .catch((error) => {
    console.error("Fetch error:", error);
  });
}


