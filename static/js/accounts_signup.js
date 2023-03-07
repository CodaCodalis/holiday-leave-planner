$(document).ready(function() {
        $('#id_division').change(function() {
            var divisionId = $(this).val();
            if (divisionId) {
              $.ajax({
                url: '/accounts/get_teams/' + divisionId,
                success: function(data) {
                  console.log(data);
                  $('#id_team').html(data);
                  $('#id_team').prop('disabled', false);
                }
              });
            } else {
                $('#id_team').html('');
                $('#id_team').prop('disabled', true);
            }
        });
});