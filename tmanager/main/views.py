from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Material, Saller
from .serializers import UserSerializer, SallerSerializer, MaterialSerializer

# Главная страница
def index(request):
    return render(request, 'main/index.html')

# Страница регистрации
def registr(request):
    return render(request, 'main/registr.html')

# Страница входа
def loginn(request):
    return render(request, 'main/loginn.html')

# Страница материалов
def materials(request):
    if request.method == 'POST':
        # Обрабатываем POST-запрос для добавления нового материала
        name = request.POST.get('name')
        price = request.POST.get('price')

        # Проверяем, что все обязательные поля заполнены
        if not name or not price:
            return render(request, 'main/materials.html', {'error': "Название и цена обязательны."})

        # Получаем текущего продавца (Saller), связанного с авторизованным пользователем
        try:
            saller = Saller.objects.get(user=request.user)
            Material.objects.create(
                name_n=name,
                price=price,
                saller=saller  # Правильная связь с продавцом
            )
            return redirect('materials')  # Перенаправляем на страницу материалов
        except Saller.DoesNotExist:
            return render(request, 'main/materials.html', {'error': "Продавец не найден."})

    # Получаем все материалы, созданные текущим продавцом
    materials = Material.objects.filter(saller__user=request.user)

    return render(request, 'main/materials.html', {'materials': materials})


# Регистрация нового продавца
class RegisterView(generics.CreateAPIView):
    def post(self, request):
        user_data = request.data

        # Проверяем, существуют ли необходимые поля
        required_fields = ['username', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in user_data:
                return Response({"message": f"Поле {field} обязательно"}, status=400)

        # Создаем пользователя
        user = User.objects.create_user(
            username=user_data['username'], 
            password=user_data['password'],
            first_name=user_data['first_name'],  
            last_name=user_data['last_name']     
        )

        # Создаем сущность продавца (Saller)
        saller = Saller.objects.create(
            user=user, 
            first_name=user_data['first_name'], 
            last_name=user_data['last_name']
        )

        return Response({"message": "Пользователь успешно зарегистрирован"}, status=201)


# Вход и получение JWT токенов
class LoginView(generics.CreateAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Проверка наличия обязательных полей
        if not username or not password:
            return Response({"message": "Логин и пароль обязательны"}, status=400)

        # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)

        return Response({"message": "Неверные данные для входа"}, status=400)


# Список материалов и добавление нового материала
class MaterialListCreateView(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            saller = Saller.objects.get(user=self.request.user)
            serializer.save(saller=saller)
        except Saller.DoesNotExist:
            return Response({"message": "Продавец не найден"}, status=400)