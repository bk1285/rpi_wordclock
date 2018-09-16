$(document).ready(function() {
    $.ajax({
        url: '/api/plugins',
        type : 'GET'
    })
    .done(function(data) {
        $("#pluginDropdown option").remove();
        $.each(data.plugins, function(index, item) {
            $("#pluginDropdown").append(
                $("<option></option>")
                    .text(item.pretty_name)
                    .val(item.name)
            );
        });
    });
    $.ajax({
            url: '/api/plugin',
            type : 'GET'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
                $('#pluginList').text("Error").show();
            }
            else {
                $('#pluginList').text(data.plugin.description).show();
                $("#pluginDropdown").val(data.plugin.name)
            }
        });

    $('select').on('change', function() {
		$.ajax({
			data : '{"name" : "' + this.value + '"}',
			type : 'POST',
			contentType: "application/json",
			url : '/api/plugin'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
				$('#pluginList').text("Error").show();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}
         });
        $.ajax({
            url: '/api/plugin',
			type : 'GET'
        })
        .done(function(data) {
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
                $('#pluginList').text("Error").show();
            }
            else {
                $('#pluginList').text(data.plugin.description).show();
                $("#pluginDropdown").val(data.plugin.name)
            }
        });
    });
});
