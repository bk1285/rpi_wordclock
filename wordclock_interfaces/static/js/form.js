$(document).ready(function() {
    $.ajax({
            url: '/get/list',
			type : 'POST'
            })
            .done(function(data) {
                $("#pluginDropdown option").remove();
                $.each(data.PLUGINS, function(index, item) {
                    $("#pluginDropdown").append(
                        $("<option></option>")
                            .text(item.PRETTY_NAME)
                            .val(item.NAME)
                    );
                });
            });
    $.ajax({
            url: '/get/active',
			type : 'POST'
            })
            .done(function(data) {
                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $('#successAlert').hide();
                    $('#pluginList').text("Error").show();
                }
                else {
                    $('#pluginList').text(data.DESCRIPTION).show();
                    $("#pluginDropdown").val(data.NAME)
                }
            });

    $('select').on('change', function() {
		$.ajax({
			data : {
				name : this.value
			},
			type : 'POST',
			url : '/set/plugin'
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
            url: '/get/active',
			type : 'POST'
            })
            .done(function(data) {
                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $('#successAlert').hide();
                    $('#pluginList').text("Error").show();
                }
                else {
                    $('#pluginList').text(data.DESCRIPTION).show();
                    $("#pluginDropdown").val(data.NAME)
                }
            });
    });
});
