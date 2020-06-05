function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
};

function load(evt) {
    openTab(event, 'Sensor');
    tablinks = document.getElementsByClassName("tablinks");

    tablinks[0].className += " active"

    getValue();
};

$(document).ready(function () {
    $('#button').click(function () {
        var data = $("#form_sensor").serializeArray();

        var json_data = new Object();

        //console.log(typeof(data));
        console.log(data);

        for (var i = 0; i < data.length; i++) {
            console.log(data[i]["name"], data[i]["value"]);
            //json_data.set(data[i]["name"], data[i]["value"])
            json_data[data[i]["name"]] = data[i]["value"];
        }

        json_data = JSON.stringify(json_data)

        $.ajax({
            url: "/sensors",
            type: "POST",
            datatype: 'json',
            contentType: "application/json",
            data: json_data,
            processData: false,
            success: function (response) {
                var json = JSON.parse(response)
                var str = JSON.stringify(json, null, 2);
                $("#data_json").text(str);
            }
        })
    });
});

function getValue() {
    $.ajax({
        url: "/sensors",
        type: "get",
        success: function (response) {
            var json = JSON.parse(response)
            var str = JSON.stringify(json, null, 2);
            $("#data_json").text(str);
        },
        error: function (xhr) {
            alert(xhr)
        }
    });
};

function getForm()
{
    var $form = $(this).parents('form');
    var id = $form.attr('id');
    console.log($form);
};