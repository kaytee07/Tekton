function getCourses (){
allcourses = document.querySelector('select#course')

const url = `http://localhost:5001/api/v1/allcourses`;
console.log(url)
const requestOptions = {
    method: "GET",
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
      console.log("Response data:", responseData);
      let newData = JSON.stringify(responseData)
      localStorage.setItem('data', newData)
      let retrievedValue = localStorage.getItem('data');
      let html = ""
      for (let value of responseData) {
          html += `
                <option>${value['name']}</option>
           `
      }
      allcourses.innerHTML = html;
  })
  .catch((error) => {
    console.error("Fetch error:", error);
  });
}
getCourses()
