/**
 * Created by Vinicius on 18/10/2014.
 */
$(document).ready(function () {

     var $setorInput = $('#setorInput');
     var $linhaInput = $('#linhaInput');
     var $dataInput = $('#dataInput');
     var $comportamentoInput = $('#comportamentoInput');
     var $nomeInput = $('#nomeInput');
     var $ajaxLoader = $('#ajax-loader');
     var $novoform = $('#novo-obs-botao');

       $('#form-div').hide();

    $novoform.click(function () {

        $('#form-div').toggle('slow');

    });



    function exibirobs(observacoe) {
        console.log(observacoe);

         var template = '<tr id="tr' + observacoe.id + '" ><td></td>' +

             '<td>' + observacoe.creation + '</td>' +
             '<td>' + observacoe.setor + '</td>' +
             '<td>' + observacoe.linha + '</td>' +
             '<td>' + observacoe.data + '</td>' +
             '<td>' + observacoe.comportamento + '</td>' +
             '<td>' + observacoe.nome + '</td>' ;
        if(observacoe.dono_flag){
            template=template+'<td><button id="bt' + observacoe.id + '" class="btn btn-danger btn-sm"><i class="glyphicon glyphicon-trash"></i></button></td>' +
             '</tr>';

        }else{

        }


         $corpoTabela.prepend(template);

      var $linhaTabela = $('#tr' + observacoe.id);
      $linhaTabela.hide();
        $linhaTabela.fadeIn();
        $('#bt' + observacoe.id).click(function () {
            $.post('/observacoes/rest/delete', {'observacoe_id': observacoe.id}).success(function(){
               $linhaTabela.remove();
           }).error(function () {
               alert('Não foi possível apagar a observação nesse momento');
                $linhaTabela.fadeIn();
             });
             $linhaTabela.fadeOut();
        });
     }


    $.post('/observacoes/rest').success(function (observacoes) {
         observacoes.forEach(exibirobs);
     });
    var $salvarObsBtn = $('#salvar-obs-btn');






    var $corpoTabela = $('#corpo-tabela');

     $salvarObsBtn.click(function () {
         var data = {setor: $setorInput.val(),
             linha: $linhaInput.val(),
             data: $dataInput.val(),
             comportamento: $comportamentoInput.val(),
             nome: $nomeInput.val()};

        $ajaxLoader.show();
        $salvarObsBtn.hide();
        $.post('/observacoes/rest/save', data).success(function (observacoe) {
             $setorInput.val('');
             $linhaInput.val('');
             $dataInput.val('');
             $comportamentoInput.val('');
             $nomeInput.val('');
            exibirobs(observacoe);}).error(function(erros){

            console.log(erros);


        }).always(function(){
            $ajaxLoader.hide();
            $salvarObsBtn.show();
        });
     });
 });