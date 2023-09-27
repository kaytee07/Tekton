student_btn = document.querySelector('form.course_cohort button')

student_btn.addEventListener('click', function (event) {
    event.preventDefault()
    getstudent()
})

getCohorts()

function getstudent (){
get_cohort_no = document.querySelector('#cohort').value;
get_course_name = document.querySelector('#course').value;
get_std_html = document.querySelector('.std_headers');
    
cohort_no = Number(get_cohort_no.split(" ")[1])
const url = `http://localhost:5001/api/v1/students/${cohort_no}/${get_course_name}`;
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
      console.log("Response data:", responseData);
      let newData = JSON.stringify(responseData)
      localStorage.setItem('data', newData)
      let retrievedValue = localStorage.getItem('data');
      let html = ""
      for (let value of responseData) {
	  html += `
                <div class="student_details">
                <h4 class="name">${value.first_name} ${value.last_name}</h4>
 
                <div class="graduated">
                    <label for="checkbox">graduated</label>:</label>
                    <input type="checkbox" id="checkbox" name="checkbox">
                </div>
            </div>
           `
      }
      get_std_html.innerHTML = html
  })
  .catch((error) => {
    console.error("Fetch error:", error);
  });
}

function getCohorts (){
allcohorts = document.querySelector('select#cohort')
    
const url = `http://localhost:5001/api/v1/allcohorts`;
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
      console.log("Response data:", responseData);
      let newData = JSON.stringify(responseData)
      localStorage.setItem('data', newData)
      let retrievedValue = localStorage.getItem('data');
      let html = ""
      for (let value of responseData) {
	  console.log(value['cohort_no'])
	  html += `
                <option>Cohort ${value['cohort_no']}</option>
           `
      }
      allcohorts.innerHTML = html;
  })
   .then((data)=> {
       getCourses()
   })
   .then((data)=> {
  
   })
  .catch((error) => {
    console.error("Fetch error:", error);
  });
}


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
	  console.log(value['name'])
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


