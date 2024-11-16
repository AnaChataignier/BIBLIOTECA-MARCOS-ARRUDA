# biblioteca/views.py
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Livro
from .forms import LivroForm
from .serializers import LivroSerializer
from urllib.parse import unquote
from django.contrib import messages



def pagina_inicial(request):
    livros = Livro.objects.all()
    categorias = Livro.objects.values("categoria").annotate(contagem=Count("categoria"))
    categorias = [
        {"nome": c["categoria"], "contagem": c["contagem"]} for c in categorias
    ]

    context = {
        "livros": livros,
        "categorias": categorias,
    }
    return render(request, "biblioteca/pagina_inicial.html", context)


def buscar(request):
    parametro = request.GET.get("query", None)

    if parametro:
        livros = Livro.objects.filter(
            Q(titulo__icontains=parametro)
            | Q(autor__icontains=parametro)
            | Q(categoria__icontains=parametro)
            | Q(ano__icontains=parametro)
        )

        categorias = Livro.objects.values("categoria").annotate(
            contagem=Count("categoria")
        )
        categorias = [
            {"nome": c["categoria"], "contagem": c["contagem"]} for c in categorias
        ]
        if livros.exists():  # Verifica se há resultados
            serializer = LivroSerializer(livros, many=True)

            context = {
                "livros": serializer.data,
                "categorias": categorias,
            }

            return render(request, "biblioteca/pagina_inicial.html", context)
        else:
            # Se não houver resultados
            return render(
                request,
                "biblioteca/pagina_inicial.html",
                {"mensagem_erro": "Nenhum livro encontrado para a busca especificada."},
            )
    else:
        # Caso o parâmetro de busca não tenha sido informado
        return render(
            request,
            "biblioteca/pagina_inicial.html",
            {"mensagem_erro": "Por favor, forneça um termo de busca."},
        )


def adicionar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)  # Cria o objeto sem salvar no banco ainda
            
            # Preenchendo campos nulos com "Não informado"
            if not livro.titulo:
                livro.titulo = "Não informado"
            if not livro.autor:
                livro.autor = "Não informado"
            if not livro.categoria:
                livro.categoria = "Não informado"
            if not livro.editora:
                livro.editora = "Não informado"
            if not livro.ano:
                livro.ano = "Não informado"
            livro.save()
            messages.success(request, "Livro adicionado com sucesso!")
            return redirect(
                "pagina_inicial"
            )  # Redireciona para a página inicial após adicionar o livro
    else:
        form = LivroForm()

    return render(request, "biblioteca/adicionar_livro.html", {"form": form})


def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)  # Busca o livro pelo ID (pk)

    if request.method == "POST":
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()  # Atualiza o livro no banco de dados
            messages.success(request, "Livro alterado com sucesso!")
            return redirect(
                "pagina_inicial"
            )  # Redireciona para a página inicial após salvar
    else:
        form = LivroForm(instance=livro)  # Preenche o formulário com os dados do livro

    return render(
        request, "biblioteca/editar_livro.html", {"form": form, "livro": livro}
    )


def deletar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if request.method == "POST":
        livro.delete()
        messages.success(request, "Livro deletado com sucesso!")
        return redirect(
            "pagina_inicial"
        )  # Redireciona para onde você achar melhor após a exclusão
    else:
        # Caso o método não seja POST, você pode redirecionar ou retornar uma página de erro.
        return redirect("pagina_inicial")


def livros_por_categoria(request, categoria):
    categoria = unquote(categoria)
    livros = Livro.objects.filter(categoria=categoria)
    categorias = Livro.objects.values("categoria").annotate(contagem=Count("categoria"))
    categorias = [
        {"nome": c["categoria"], "contagem": c["contagem"]} for c in categorias
    ]

    context = {
        "livros": livros,
        "categorias": categorias,
        "categoria_selecionada": categoria,
    }
    return render(request, "biblioteca/pagina_inicial.html", context)


def livros_por_autor(request, autor_nome):
    autor_nome = unquote(
        autor_nome
    )  # Decodifica o nome do autor, caso tenha caracteres especiais
    livros = Livro.objects.filter(
        autor__icontains=autor_nome
    )  # Filtra livros pelo autor
    categorias = Livro.objects.values("categoria").annotate(contagem=Count("categoria"))
    categorias = [
        {"nome": c["categoria"], "contagem": c["contagem"]} for c in categorias
    ]

    context = {
        "livros": livros,
        "autor_selecionado": autor_nome,
        "categorias": categorias,
    }
    return render(request, "biblioteca/pagina_inicial.html", context)


def sugestoes(request):
    query = request.GET.get("q", "")  # 'q' é o parâmetro de busca
    if query:
        # Busca por autores e categorias no modelo Livro
        autores = (
            Livro.objects.filter(autor__icontains=query)
            .values_list("autor", flat=True)
            .distinct()
        )
        categorias = (
            Livro.objects.filter(categoria__icontains=query)
            .values_list("categoria", flat=True)
            .distinct()
        )

        # Retorna as sugestões como listas
        return JsonResponse({"autores": list(autores), "categorias": list(categorias)})
    return JsonResponse({"autores": [], "categorias": []})
