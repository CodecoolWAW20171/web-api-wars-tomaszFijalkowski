$('#residentsModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget)
    let planetName = button.data('name')
    let residents = button.data('residents').replace(/'/g, '"')
    let text = button.data('ammount') == "many" ? "Residents" : "Resident"
    let modal = $(this)
    let modalTable = ""

    document.getElementById("modalTable").innerHTML = ""
    modal.find('.modal-title').text(text + ' of ' + planetName)

    $.parseJSON(residents).forEach(function (resident) {

        function getData() {
            return $.getJSON(resident, function (response) {
                return response
            });
        }

        $.when(getData()).done(function (data) {
            let height = data["height"] == "unknown" ? data["height"] : data["height"] + " cm"
            let mass = data["mass"] == "unknown" ? data["mass"] : data["mass"] + " kg"
            modalTable += "<tr>\
                            <td>" + data["name"] + "</td> \
                            <td>" + height + "</td> \
                            <td>" + mass + "</td> \
                            <td>" + data["skin_color"] + "</td> \
                            <td>" + data["hair_color"] + "</td> \
                            <td>" + data["eye_color"] + "</td> \
                            <td>" + data["birth_year"] + "</td> \
                            <td>" + data["gender"] + "</td> \
                           </tr>"
            document.getElementById("modalTable").innerHTML = modalTable
        });
    });
})


$('#statisticsModal').on('show.bs.modal', function (event) {
    let statisticsTable = ""
    document.getElementById("statisticsLink").innerHTML = 'Statistics'
    req = $.ajax({
        url: '/statistics',
        type: 'POST',
    });
    req.done(function (data) {
        data.forEach(function (data) {
            statisticsTable += "<tr>\
                        <td>" + data["planet_name"] + "</td> \
                        <td>" + data["votes"] + "</td> \
                       </tr>"
        })
        document.getElementById("statisticsTable").innerHTML = statisticsTable
    });
    $(this).find('.modal-title').text("Vote statistics")
});


function vote(button) {
    let voteData = {
        planetId: $(button).data('planetId'),
        planetName: $(button).data('planetName'),
        userId: $(button).data('userId')
    }
    $.ajax({
        url: '/vote',
        type: 'POST',
        data: voteData,
        success: function (response) {
            $('#main').text(response)
            document.getElementById("statisticsLink").innerHTML = 'Statistics <span id="statisticsBadge" class="badge badge-primary pt-1">New</span>'
            voteSuccess(button)
        }
    })
}


function rowMouseOver(row) {
    document.getElementById("vote_" + row).style.visibility = "visible"
}


function rowMouseOut(row) {
    document.getElementById("vote_" + row).style.visibility = "hidden"
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function voteSuccess(button) {
    button.setAttribute("class", "btn btn-outline-success vote btn-sm")
    document.getElementById("statisticsBadge").style.transition = "0.3s"
    document.getElementById("statisticsBadge").setAttribute("class", "badge badge-success pt-1")
    await sleep(300);
    button.setAttribute("class", "btn btn-outline-primary vote btn-sm")
    document.getElementById("statisticsBadge").setAttribute("class", "badge badge-primary pt-1")
}