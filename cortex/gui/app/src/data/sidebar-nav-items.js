
function SidebarItems(){
  let users = [];
  users.push(
    {
      title: "Users",
      htmlBefore: '<i class="material-icons">table_chart</i>',
      to: "/tables",
    });
  fetch('/users').then(res => res.json()).then(data => {
    for (let i = 0; i < data.length; i++) {
      let user = data[i];
      users.push(
        {
          title: user["username"],
          to: "/users/" + user["user_id"],
          htmlBefore: '<i class="material-icons">person</i>',
          htmlAfter: ""
        });
    }
  });

  return users;
}

export default SidebarItems;
