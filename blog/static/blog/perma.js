
$(document).ready(function(){
$("#like").click(function()
    {
      console.log("000");
      $.ajax({
        type:'POST',
        url:'/post/like/',
        data:{
          'post_id':$("#xyz").attr('data-id') },
        dataType:"json",
        success:function(response){
          $("#total_likes").text(response.like_count);
          $("#like").text(response.msg);
        },
        error:function()
        {
          console.log("1111")
        }
      });
    });
      // print all comments

    $("#comments").click(function(){
      $.ajax({
        type:'GET',
        url:'/post/comments/',
        data:{
          'postid':$("#xyz").attr('data-id')
        },
        dataType:"json",
        success:function(alldata){
          var data=$('<table>')
          for(var i=0; i<alldata.length;i++)
          {
            data+=('<tr> <td><b>'+ alldata[i][0]+'\xa0\xa0'+ '</b></td><td>'+alldata[i][1] + '</td></tr>')
          }
          data+=$('</table>')
          $("#cmnttable").html(data)
        }
      });
    });
    $("#comments").click(function()
    {
      $("#tb").slideDown("Medium");
    });

  // submit comment

  var input = document.getElementById("x2");
    if(input)
    {
      input.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
       event.preventDefault();
       $.ajax({
                type:'POST',
                url:'/post/comment/',
                data:{
                  msg:$('#x2').val(),
                  postid:$("#xyz").attr("data-id"),
                },
                dataType:"json",
                success:function(response){
                  if(response.reply==0)
                  {
                    alert("Login require..");
                  }
                  document.getElementById("x2").value ="";
                }
            });
      }
    });
}
})
 