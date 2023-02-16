const tBody = document.querySelector('#tbody')

const getTasks = async() => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todo', {
      headers: {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NDMzNDcyLCJpYXQiOjE2NzY0MzMxNzIsImp0aSI6Ijg3MzlhZGNkODE4YzQ0MjM4Y2JlY2U2YTU2NzMyYjExIiwidXNlcl9pZCI6MX0.va7ximo0xgLNT6vOJqf6AVLGGfZSHHoBuW3ZOoBg9do'
      }
    })
    const data = await response.json()
    printTasks(data.results)
  } catch (error) {
    console.log(error)
  }
}

const printTasks = async(data) => {
  tBody.innerHTML = ''
  data.forEach(task => {
    tBody.innerHTML += 
    `
    <tr>
      <td>${task.title}</td>
      <td>${task.body}</td>
      <td>${task.created_at}</td>
      <td>${task.done_at}</td>
      <td>${task.updated_at}</td>
      <td>${task.deleted_at}</td>
      <td>${task.status}</td>
      </tr>
    `
  })
}

getTasks()