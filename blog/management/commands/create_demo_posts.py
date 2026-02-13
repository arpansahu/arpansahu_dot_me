"""
Management command to create demo blog posts across multiple categories.
Helps Google AdSense verification by providing real content with proper
category/tag linking and SEO metadata.

Usage:
    python manage.py create_demo_posts
    python manage.py create_demo_posts --delete   # Remove all demo posts first
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import BlogPost, Category, Tag
from account.models import Account


CATEGORIES = [
    {
        'name': 'Technology',
        'slug': 'technology',
        'description': 'Latest trends in technology, software engineering, and innovation.',
    },
    {
        'name': 'Web Development',
        'slug': 'web-development',
        'description': 'Frontend, backend, and full-stack web development tutorials and insights.',
    },
    {
        'name': 'DevOps & Cloud',
        'slug': 'devops-cloud',
        'description': 'CI/CD pipelines, containerization, Kubernetes, and cloud infrastructure.',
    },
    {
        'name': 'Python Programming',
        'slug': 'python-programming',
        'description': 'Python tips, tricks, libraries, and best practices for developers.',
    },
    {
        'name': 'Career & Productivity',
        'slug': 'career-productivity',
        'description': 'Career advice, productivity hacks, and professional growth for developers.',
    },
]

TAGS = [
    'Python', 'Django', 'JavaScript', 'React', 'Docker', 'Kubernetes',
    'CI/CD', 'AWS', 'PostgreSQL', 'Redis', 'REST API', 'Machine Learning',
    'Linux', 'Git', 'Nginx', 'Celery', 'WebSockets', 'Security',
    'Performance', 'Testing',
]

POSTS = [
    # ── Technology ──────────────────────────────────────────────
    {
        'title': 'Understanding Microservices Architecture in 2026',
        'slug': 'understanding-microservices-architecture-2026',
        'category_slug': 'technology',
        'tags': ['Docker', 'Kubernetes', 'REST API', 'AWS'],
        'excerpt': 'A comprehensive guide to designing, building, and deploying microservices in modern software systems.',
        'meta_description': 'Learn microservices architecture patterns, best practices, and deployment strategies for 2026.',
        'meta_keywords': 'microservices, architecture, docker, kubernetes, api gateway',
        'sequence': 1,
        'content': '''
<h2>What Are Microservices?</h2>
<p>Microservices architecture is an approach to building applications as a collection of small, autonomous services modeled around a business domain. Unlike monolithic applications, each microservice runs independently, communicates over well-defined APIs, and can be deployed, scaled, and maintained separately.</p>

<h3>Key Principles</h3>
<ul>
    <li><strong>Single Responsibility:</strong> Each service handles one specific business capability.</li>
    <li><strong>Decentralized Data Management:</strong> Each service manages its own database.</li>
    <li><strong>Fault Isolation:</strong> Failure in one service doesn't cascade to others.</li>
    <li><strong>Independent Deployment:</strong> Services can be updated without redeploying the entire application.</li>
</ul>

<h3>Communication Patterns</h3>
<p>Microservices communicate using either synchronous (REST, gRPC) or asynchronous (message queues, event streaming) patterns. Choosing the right communication method depends on latency requirements and data consistency needs.</p>

<pre><code class="language-python"># Example: Simple REST API with Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'user-service',
        'version': '2.1.0'
    })
</code></pre>

<h3>When to Use Microservices</h3>
<p>Microservices shine in large teams working on complex applications where independent scaling and deployment are critical. For smaller projects, a well-structured monolith might be more pragmatic. The key is to evaluate your team size, deployment frequency, and scaling requirements before committing to a distributed architecture.</p>

<h3>Conclusion</h3>
<p>Microservices offer tremendous flexibility but come with operational complexity. Invest in observability, automated testing, and CI/CD pipelines early to reap the benefits without drowning in distributed systems challenges.</p>
''',
    },
    {
        'title': 'The Rise of AI-Powered Development Tools',
        'slug': 'rise-of-ai-powered-development-tools',
        'category_slug': 'technology',
        'tags': ['Machine Learning', 'Python', 'Performance'],
        'excerpt': 'How AI assistants, code generation, and intelligent testing are reshaping the software development landscape.',
        'meta_description': 'Explore AI-powered development tools transforming coding, testing, and deployment in 2026.',
        'meta_keywords': 'ai development tools, code generation, copilot, machine learning, testing',
        'sequence': 2,
        'content': '''
<h2>AI Is Changing How We Write Code</h2>
<p>The integration of artificial intelligence into the developer workflow has accelerated dramatically. From intelligent code completion to automated bug detection, AI tools are becoming indispensable partners in software engineering.</p>

<h3>Categories of AI Development Tools</h3>
<ol>
    <li><strong>Code Generation:</strong> Tools like GitHub Copilot and Claude can generate entire functions, classes, and even complex architectures from natural language descriptions.</li>
    <li><strong>Automated Testing:</strong> AI-powered test generators analyze your codebase and create comprehensive test suites automatically.</li>
    <li><strong>Code Review:</strong> Intelligent reviewers catch bugs, security vulnerabilities, and performance issues before they reach production.</li>
    <li><strong>Documentation:</strong> AI can generate and maintain documentation that stays synchronized with your code.</li>
</ol>

<h3>Practical Example: AI-Assisted Testing</h3>
<pre><code class="language-python"># AI-generated test for a user registration endpoint
import pytest
from django.test import TestCase
from django.urls import reverse

class TestUserRegistration(TestCase):
    def test_valid_registration(self):
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_duplicate_email_rejected(self):
        # First registration
        self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'user1',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        # Duplicate should fail
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'user2',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered
</code></pre>

<h3>The Human Element</h3>
<p>AI tools augment developers rather than replace them. Critical thinking, system design, and understanding business requirements remain uniquely human skills. The developers who thrive will be those who learn to collaborate effectively with AI assistants.</p>
''',
    },

    # ── Web Development ────────────────────────────────────────
    {
        'title': 'Building a Full-Stack Blog with Django and React',
        'slug': 'building-fullstack-blog-django-react',
        'category_slug': 'web-development',
        'tags': ['Django', 'React', 'JavaScript', 'REST API', 'PostgreSQL'],
        'excerpt': 'Step-by-step guide to building a production-ready blog application with Django REST Framework backend and React frontend.',
        'meta_description': 'Build a full-stack blog with Django REST Framework and React. Complete tutorial with authentication and deployment.',
        'meta_keywords': 'django, react, full stack, blog, rest api, postgresql',
        'sequence': 1,
        'content': '''
<h2>Project Overview</h2>
<p>In this tutorial, we'll build a complete blog application with a Django REST Framework backend and a React frontend. The application will feature user authentication, CRUD operations for posts, categories, tags, and a responsive design.</p>

<h3>Backend: Django REST Framework</h3>
<p>Django provides an excellent foundation for building robust APIs. Combined with Django REST Framework, we get serialization, authentication, and viewsets out of the box.</p>

<pre><code class="language-python"># blog/serializers.py
from rest_framework import serializers
from .models import BlogPost, Category

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']

class BlogPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'excerpt', 'content',
                  'category', 'reading_time', 'published_date']

    def get_reading_time(self, obj):
        return obj.get_reading_time()
</code></pre>

<h3>Frontend: React Components</h3>
<p>The React frontend consumes the API and renders the blog with a clean, responsive interface. We use React Router for navigation and React Query for data fetching.</p>

<pre><code class="language-javascript">// components/BlogList.jsx
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';

export default function BlogList() {
    const { data: posts, isLoading } = useQuery({
        queryKey: ['posts'],
        queryFn: () => fetch('/api/posts/').then(r => r.json())
    });

    if (isLoading) return &lt;div&gt;Loading...&lt;/div&gt;;

    return (
        &lt;div className="blog-grid"&gt;
            {posts.map(post => (
                &lt;article key={post.id}&gt;
                    &lt;Link to={`/blog/${post.slug}`}&gt;
                        &lt;h2&gt;{post.title}&lt;/h2&gt;
                    &lt;/Link&gt;
                    &lt;p&gt;{post.excerpt}&lt;/p&gt;
                    &lt;span&gt;{post.reading_time} min read&lt;/span&gt;
                &lt;/article&gt;
            ))}
        &lt;/div&gt;
    );
}
</code></pre>

<h3>Deployment</h3>
<p>We deploy the Django backend with Gunicorn behind Nginx, and the React frontend as static files served by the same Nginx instance. PostgreSQL handles the database, and Redis provides caching for frequently accessed posts.</p>
''',
    },
    {
        'title': 'Modern CSS Techniques Every Developer Should Know',
        'slug': 'modern-css-techniques-developers-should-know',
        'category_slug': 'web-development',
        'tags': ['JavaScript', 'Performance'],
        'excerpt': 'From CSS Grid and Container Queries to the latest selectors — master the CSS features that make responsive design effortless.',
        'meta_description': 'Master modern CSS techniques including Grid, Container Queries, :has() selector, and CSS nesting.',
        'meta_keywords': 'css, grid, flexbox, container queries, responsive design, css nesting',
        'sequence': 2,
        'content': '''
<h2>CSS Has Evolved Dramatically</h2>
<p>CSS in 2026 is remarkably powerful. Features that once required JavaScript or complex workarounds are now achievable with pure CSS. Let's explore the most impactful modern CSS techniques.</p>

<h3>1. CSS Grid for Complex Layouts</h3>
<p>CSS Grid enables two-dimensional layouts that were previously impossible without frameworks. It's now supported in all modern browsers.</p>

<pre><code class="language-css">.blog-layout {
    display: grid;
    grid-template-columns: 1fr 300px;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "header  header"
        "content sidebar"
        "footer  footer";
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

@media (max-width: 768px) {
    .blog-layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "content"
            "sidebar"
            "footer";
    }
}
</code></pre>

<h3>2. Container Queries</h3>
<p>Container queries let components respond to their container's size rather than the viewport, making truly reusable components possible.</p>

<pre><code class="language-css">.card-container {
    container-type: inline-size;
    container-name: card;
}

@container card (min-width: 400px) {
    .card {
        display: grid;
        grid-template-columns: 200px 1fr;
    }
}
</code></pre>

<h3>3. The :has() Selector</h3>
<p>Often called the "parent selector," <code>:has()</code> lets you style elements based on their children — something CSS couldn't do before.</p>

<pre><code class="language-css">/* Style a card differently if it has an image */
.card:has(img) {
    grid-template-rows: 200px 1fr;
}

/* Highlight form fields with errors */
.form-group:has(.error) label {
    color: red;
}
</code></pre>

<h3>Conclusion</h3>
<p>Modern CSS eliminates the need for many JavaScript-based layout solutions. By leveraging Grid, Container Queries, and new selectors, you can build responsive, maintainable interfaces with less code and better performance.</p>
''',
    },

    # ── DevOps & Cloud ─────────────────────────────────────────
    {
        'title': 'Complete Guide to CI/CD with Jenkins and Kubernetes',
        'slug': 'complete-guide-cicd-jenkins-kubernetes',
        'category_slug': 'devops-cloud',
        'tags': ['CI/CD', 'Kubernetes', 'Docker', 'Git', 'Nginx'],
        'excerpt': 'Set up a production-grade CI/CD pipeline using Jenkins, Docker, and Kubernetes from scratch.',
        'meta_description': 'Build a CI/CD pipeline with Jenkins, Docker, and Kubernetes. Complete setup guide with automated testing and deployment.',
        'meta_keywords': 'jenkins, kubernetes, cicd, docker, deployment, automation',
        'sequence': 1,
        'content': '''
<h2>Why CI/CD Matters</h2>
<p>Continuous Integration and Continuous Deployment (CI/CD) automates the process of testing, building, and deploying your applications. A well-designed pipeline catches bugs early, ensures consistent deployments, and dramatically reduces time-to-production.</p>

<h3>Pipeline Architecture</h3>
<p>Our pipeline follows these stages:</p>
<ol>
    <li><strong>Checkout:</strong> Pull the latest code from the Git repository.</li>
    <li><strong>Unit Tests:</strong> Run the full test suite in an isolated Docker container.</li>
    <li><strong>UI Tests:</strong> Execute Playwright-based browser tests against a running instance.</li>
    <li><strong>Build Image:</strong> Create a Docker image with the application.</li>
    <li><strong>Push Image:</strong> Push to a container registry.</li>
    <li><strong>Deploy:</strong> Rolling update on Kubernetes cluster.</li>
    <li><strong>Health Check:</strong> Verify the deployment is healthy.</li>
</ol>

<h3>Jenkinsfile Example</h3>
<pre><code class="language-groovy">pipeline {
    agent any

    stages {
        stage('Test') {
            agent {
                docker { image 'python:3.11' }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --tb=short -v'
            }
        }

        stage('Build & Push') {
            steps {
                script {
                    def img = docker.build("myapp:${env.BUILD_NUMBER}")
                    docker.withRegistry('https://registry.example.com', 'registry-creds') {
                        img.push()
                        img.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh "kubectl set image deployment/myapp myapp=myapp:${env.BUILD_NUMBER}"
                sh 'kubectl rollout status deployment/myapp --timeout=120s'
            }
        }
    }
}
</code></pre>

<h3>Kubernetes Deployment</h3>
<p>Our Kubernetes setup uses Deployments with rolling updates, ConfigMaps for environment variables, and Services with NodePort for internal access behind an Nginx reverse proxy.</p>

<h3>Monitoring & Alerts</h3>
<p>Integrate Sentry for error tracking and Prometheus for metrics. Set up alerts for deployment failures, high error rates, and resource exhaustion to catch problems before users do.</p>
''',
    },
    {
        'title': 'Docker Best Practices for Production Applications',
        'slug': 'docker-best-practices-production',
        'category_slug': 'devops-cloud',
        'tags': ['Docker', 'Linux', 'Security', 'Performance', 'Nginx'],
        'excerpt': 'Optimize your Docker images for security, performance, and reliability in production environments.',
        'meta_description': 'Learn Docker best practices for production: multi-stage builds, security hardening, and optimization techniques.',
        'meta_keywords': 'docker, production, best practices, multi-stage builds, security, optimization',
        'sequence': 2,
        'content': '''
<h2>Production-Ready Docker Images</h2>
<p>Building Docker images for development is easy. Building images that are secure, small, and performant for production requires deliberate best practices.</p>

<h3>1. Multi-Stage Builds</h3>
<p>Multi-stage builds separate the build environment from the runtime environment, resulting in dramatically smaller final images.</p>

<pre><code class="language-dockerfile"># Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
</code></pre>

<h3>2. Security Hardening</h3>
<ul>
    <li><strong>Run as non-root:</strong> Always use <code>USER</code> directive to avoid running as root.</li>
    <li><strong>Scan for vulnerabilities:</strong> Use tools like Trivy or Snyk to scan images before deployment.</li>
    <li><strong>Pin base images:</strong> Use specific version tags, never <code>latest</code> in production.</li>
    <li><strong>Minimize attack surface:</strong> Use minimal base images like <code>-slim</code> or <code>-alpine</code> variants.</li>
</ul>

<h3>3. Layer Optimization</h3>
<p>Docker caches layers, so order your Dockerfile instructions from least to most frequently changed. Copy dependency files first, install dependencies, then copy application code.</p>

<h3>4. Health Checks</h3>
<pre><code class="language-dockerfile">HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1
</code></pre>

<h3>Conclusion</h3>
<p>A well-optimized Docker image can be 80% smaller and significantly more secure than a naive build. Invest time in your Dockerfile — it pays dividends in deployment speed and security posture.</p>
''',
    },

    # ── Python Programming ─────────────────────────────────────
    {
        'title': 'Advanced Python: Decorators, Context Managers, and Metaclasses',
        'slug': 'advanced-python-decorators-context-managers-metaclasses',
        'category_slug': 'python-programming',
        'tags': ['Python', 'Performance', 'Testing'],
        'excerpt': 'Deep dive into Python\'s most powerful features — decorators, context managers, and metaclasses — with practical examples.',
        'meta_description': 'Master advanced Python: decorators, context managers, metaclasses with real-world examples and best practices.',
        'meta_keywords': 'python, decorators, context managers, metaclasses, advanced python',
        'sequence': 1,
        'content': '''
<h2>Beyond the Basics</h2>
<p>Python's simplicity is deceptive. Beneath its clean syntax lie powerful abstractions that, when mastered, enable elegant solutions to complex problems.</p>

<h3>Decorators</h3>
<p>Decorators modify or extend function behavior without changing the function itself. They're essential for cross-cutting concerns like logging, authentication, and caching.</p>

<pre><code class="language-python">import functools
import time

def timing(func):
    """Measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def retry(max_attempts=3, delay=1):
    """Retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@timing
@retry(max_attempts=3)
def fetch_data(url):
    import requests
    return requests.get(url).json()
</code></pre>

<h3>Context Managers</h3>
<p>Context managers ensure proper resource acquisition and release, making your code both safer and more readable.</p>

<pre><code class="language-python">from contextlib import contextmanager

@contextmanager
def database_transaction(connection):
    """Manage database transactions with automatic rollback on error."""
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

# Usage
with database_transaction(conn) as cursor:
    cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Alice",))
    cursor.execute("UPDATE stats SET user_count = user_count + 1")
</code></pre>

<h3>Metaclasses</h3>
<p>Metaclasses control class creation itself. While rarely needed, they're powerful for building frameworks, ORMs, and validation systems — Django's model system is built on metaclasses.</p>

<h3>When to Use Each</h3>
<p>Use <strong>decorators</strong> for modifying function behavior. Use <strong>context managers</strong> for resource management. Use <strong>metaclasses</strong> only when decorators and class inheritance aren't sufficient — which is rare in application code.</p>
''',
    },
    {
        'title': 'Building REST APIs with Django REST Framework',
        'slug': 'building-rest-apis-django-rest-framework',
        'category_slug': 'python-programming',
        'tags': ['Python', 'Django', 'REST API', 'PostgreSQL', 'Testing'],
        'excerpt': 'A practical guide to building robust, well-documented REST APIs using Django REST Framework with authentication and testing.',
        'meta_description': 'Complete guide to building REST APIs with Django REST Framework including authentication, serializers, and testing.',
        'meta_keywords': 'django rest framework, api, python, serializers, authentication, testing',
        'sequence': 2,
        'content': '''
<h2>Django REST Framework: The Complete Guide</h2>
<p>Django REST Framework (DRF) is the gold standard for building web APIs in Python. It provides powerful serialization, flexible authentication, and browsable APIs out of the box.</p>

<h3>Setting Up</h3>
<pre><code class="language-bash">pip install djangorestframework
pip install django-filter
pip install drf-spectacular  # OpenAPI documentation
</code></pre>

<h3>Serializers</h3>
<p>Serializers convert complex data types like Django querysets into Python data types that can be rendered as JSON. They also handle validation and deserialization.</p>

<pre><code class="language-python">from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'excerpt', 'content',
                  'author_name', 'like_count', 'published_date']
        read_only_fields = ['slug', 'published_date']

    def get_like_count(self, obj):
        return obj.likes.count()

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters.")
        return value
</code></pre>

<h3>ViewSets and Routers</h3>
<pre><code class="language-python">from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'views']

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.get_or_create(user=request.user)
        return Response({'status': 'liked'})
</code></pre>

<h3>Testing Your API</h3>
<p>DRF includes a powerful test client. Always test your serializer validation, permissions, and edge cases.</p>

<h3>Documentation</h3>
<p>Use <code>drf-spectacular</code> to auto-generate OpenAPI 3.0 documentation. This gives you interactive Swagger UI and ReDoc pages that stay synchronized with your code.</p>
''',
    },

    # ── Career & Productivity ──────────────────────────────────
    {
        'title': 'Essential Soft Skills for Software Engineers',
        'slug': 'essential-soft-skills-software-engineers',
        'category_slug': 'career-productivity',
        'tags': ['Git', 'Testing'],
        'excerpt': 'Technical skills get you hired, but soft skills drive your career forward. Learn the communication, collaboration, and leadership skills that set great engineers apart.',
        'meta_description': 'Essential soft skills for software engineers: communication, collaboration, mentoring, and technical leadership.',
        'meta_keywords': 'soft skills, software engineer, career, communication, leadership, teamwork',
        'sequence': 1,
        'content': '''
<h2>Beyond Technical Excellence</h2>
<p>The best software engineers aren't just great coders — they're effective communicators, collaborators, and problem solvers. While technical skills form the foundation, soft skills determine how far your career goes.</p>

<h3>1. Communication</h3>
<p>Clear communication is the most impactful skill you can develop. This includes:</p>
<ul>
    <li><strong>Writing clear documentation:</strong> Your future self and teammates will thank you.</li>
    <li><strong>Explaining technical concepts:</strong> Practice explaining complex ideas to non-technical stakeholders.</li>
    <li><strong>Giving constructive code reviews:</strong> Focus on teaching, not criticizing.</li>
    <li><strong>Writing effective commit messages:</strong> Describe <em>why</em>, not just <em>what</em>.</li>
</ul>

<h3>2. Collaboration</h3>
<p>Software is a team sport. Effective collaboration means:</p>
<ul>
    <li>Actively listening to different perspectives before proposing solutions.</li>
    <li>Breaking large tasks into smaller, peer-reviewable chunks.</li>
    <li>Sharing knowledge through pair programming, tech talks, and documentation.</li>
    <li>Being open to feedback and willing to change your approach.</li>
</ul>

<h3>3. Time Management</h3>
<p>Senior engineers protect their focused time while remaining accessible. Techniques that work:</p>
<ul>
    <li><strong>Time blocking:</strong> Dedicate uninterrupted hours for deep work.</li>
    <li><strong>Prioritization:</strong> Focus on impact, not just urgency.</li>
    <li><strong>Saying no:</strong> Protect your bandwidth for high-impact work.</li>
</ul>

<h3>4. Mentoring</h3>
<p>Teaching others is the fastest way to deepen your own understanding. Mentor junior developers, write blog posts, and contribute to open-source projects. The compound returns of helping others are immeasurable.</p>

<h3>Conclusion</h3>
<p>Invest in soft skills with the same intentionality you bring to learning new frameworks. The combination of technical excellence and strong interpersonal skills is what creates truly exceptional engineers.</p>
''',
    },
    {
        'title': 'Setting Up a Personal Portfolio Website That Gets You Hired',
        'slug': 'setting-up-personal-portfolio-website',
        'category_slug': 'career-productivity',
        'tags': ['Django', 'Nginx', 'Docker', 'Git', 'Security'],
        'excerpt': 'Build a professional portfolio website that showcases your projects, blog, and skills — complete with CI/CD deployment.',
        'meta_description': 'Create a personal portfolio website with Django. Complete guide including deployment, SEO, and CI/CD pipeline.',
        'meta_keywords': 'portfolio website, personal website, django, deployment, seo, career',
        'sequence': 2,
        'content': '''
<h2>Your Portfolio Is Your Best Resume</h2>
<p>A well-crafted portfolio website demonstrates your skills more effectively than any resume bullet point. It shows potential employers that you can build, deploy, and maintain real applications.</p>

<h3>Essential Sections</h3>
<ol>
    <li><strong>About:</strong> A concise professional summary highlighting your expertise and interests.</li>
    <li><strong>Projects:</strong> Showcase 4-6 of your best projects with descriptions, tech stacks, and live demos.</li>
    <li><strong>Blog:</strong> Write about your learnings — it demonstrates expertise and communication skills.</li>
    <li><strong>Resume:</strong> Offer a downloadable PDF alongside the web version.</li>
    <li><strong>Contact:</strong> Make it easy for recruiters and collaborators to reach you.</li>
</ol>

<h3>Tech Stack Recommendation</h3>
<p>For a developer portfolio, I recommend:</p>
<ul>
    <li><strong>Backend:</strong> Django — battle-tested, great admin panel, excellent ORM.</li>
    <li><strong>Database:</strong> PostgreSQL for reliability and performance.</li>
    <li><strong>Cache:</strong> Redis for session management and caching.</li>
    <li><strong>Server:</strong> Gunicorn + Nginx with SSL via Let's Encrypt.</li>
    <li><strong>Deployment:</strong> Docker + Kubernetes with Jenkins CI/CD.</li>
</ul>

<h3>SEO Basics</h3>
<pre><code class="language-html">&lt;!-- Essential meta tags for SEO --&gt;
&lt;meta name="description" content="Your professional summary"&gt;
&lt;meta name="keywords" content="python, django, developer"&gt;
&lt;meta property="og:title" content="Your Name - Software Engineer"&gt;
&lt;meta property="og:description" content="Portfolio and blog"&gt;
&lt;meta property="og:type" content="website"&gt;
&lt;link rel="canonical" href="https://yoursite.com/"&gt;
</code></pre>

<h3>Deployment Pipeline</h3>
<p>Set up a CI/CD pipeline that automatically tests, builds, and deploys your portfolio on every push to main. This not only keeps your site updated but also demonstrates your DevOps skills to potential employers.</p>

<h3>Keep It Updated</h3>
<p>A stale portfolio is worse than no portfolio. Set a monthly reminder to update projects, add new blog posts, and refresh your resume. Your portfolio should evolve as your career does.</p>
''',
    },
]


class Command(BaseCommand):
    help = 'Create demo blog posts with categories and tags for AdSense verification'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete all demo posts before recreating',
        )

    def handle(self, *args, **options):
        author = Account.objects.filter(is_superuser=True).first()
        if not author:
            self.stderr.write(self.style.ERROR('No superuser found! Create one first.'))
            return

        if options['delete']:
            slugs = [p['slug'] for p in POSTS]
            deleted, _ = BlogPost.objects.filter(slug__in=slugs).delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing demo objects'))

        # Create categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']},
            )
            cat_map[cat_data['slug']] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Category: {cat.name} [{status}]')

        # Create tags
        tag_map = {}
        for tag_name in TAGS:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-').replace('/', '-')},
            )
            tag_map[tag_name] = tag

        self.stdout.write(f'  Tags: {len(tag_map)} ready')

        # Create posts
        created_count = 0
        for post_data in POSTS:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'author': author,
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'].strip(),
                    'category': cat_map[post_data['category_slug']],
                    'status': 'published',
                    'published_date': timezone.now(),
                    'is_featured': False,
                    'enable_comments': True,
                    'meta_description': post_data['meta_description'],
                    'meta_keywords': post_data['meta_keywords'],
                    'sequence': post_data['sequence'],
                },
            )
            if created:
                post.tags.add(*[tag_map[t] for t in post_data['tags']])
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✅ Post: {post.title} → /blog/post/{post.slug}/'
                ))
            else:
                self.stdout.write(f'  ℹ️  Exists: {post.title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! {created_count} new posts created across {len(cat_map)} categories with {len(tag_map)} tags.'
        ))
        self.stdout.write(f'Visit /blog/ to see all posts.')
