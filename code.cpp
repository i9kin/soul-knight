#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef long double ld;

const ld EPS = 1e-8;

struct point {
    ld x, y;
    ll id = -1;
    
    point() {

    }    

    point(ld x_, ld y_) {
        x = x_;
        y = y_;
    } 
    friend bool operator==(const point &f, const point &s) {
        return abs(f.x - s.x) < EPS && abs(f.y - s.y) < EPS;
    }
 
    friend bool operator!=(const point &f, const point &s) {
        return !(f == s);
    }

    friend bool operator<(const point &f, const point &s) {
        if (abs(f.x - s.x) < EPS) {
            return f.y - s.y < -EPS;
        } else {
            return f.x - s.x < -EPS;
        }
    }

    friend bool operator>(const point &f, const point &s) {
        if (abs(f.x - s.x) < EPS) {
            return f.y - s.y > EPS;
        } else {
            return f.x - s.x > EPS;
        }
    }

    friend bool operator>=(const point &f, const point &s) {
        return !(f < s);
    }

    friend bool operator<=(const point &f, const point &s) {
        return !(f > s);
    }
    
    point operator - (const point &other) const {
        return point(x - other.x, y - other.y);
    }

    long long len() {
        return x * x + y * y;
    }

    ll operator * (const point &other) const{
        return x * other.y - y * other.x;
    }
};


struct Coefficient {
    ld a, b, c;

    Coefficient(ld a_, ld b_, ld c_) {
        a = a_;
        b = b_;
        c = c_;
    }

    Coefficient(point p1, point p2) {
        a = p2.y - p1.y;
        b = -(p2.x - p1.x);
        c = -(a * p1.x + b * p1.y);
    }

    friend bool operator==(const Coefficient &f, const Coefficient &s) {
        return f.a == s.a && f.b == s.b && f.c == f.c;
    }
};

struct Vector {
    point p;

    Vector(point f, point s) { // f -> s
        p = point(s.x - f.x, s.y - f.y);
    }

    Vector(point t) {
        p = t;
    }

    Vector(ld x, ld y) {
        p = {x, y};
    }

    friend Vector operator+(const Vector &f, const Vector &s) {
        return Vector(f.p.x + s.p.x, f.p.y + s.p.y);
    }

    friend Vector operator-(const Vector &f, const Vector &s) {
        return Vector(f.p.x - s.p.x, f.p.y - s.p.y);
    }

    friend ld operator*(const Vector &f, const Vector &s) {
        return f.p.x * s.p.y - f.p.y * s.p.x;
    }

    friend ld operator^(const Vector &f, const Vector &s) {
        return f.p.x * s.p.x + f.p.y * s.p.y;
    }

};

ld dist(point a, point b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

ld angle(point a, point b, point c) {
    auto Vec1 = Vector(a, c);
    auto Vec2 = Vector(a, b);
    return atan2(Vec1 * Vec2, Vec1 ^ Vec2);
}

ld angle_gr(point a, point b, point c) {
    auto Vec1 = Vector(a, c);
    auto Vec2 = Vector(a, b);
    return abs(atan2(Vec1 * Vec2, Vec1 ^ Vec2) / M_PI * 180);
}

ld point_to_vector(point p1, point p2, point p3) {
    point p; // point vector
    p.x = p2.x - p1.x;
    p.y = p2.y - p1.y;
    point pn; // point normal
    pn.x = -p.y;
    pn.y = p.x;
    point p4; // point p3 p4
    p4.x = p3.x + pn.x;
    p4.y = p3.y + pn.y;
    auto line = Coefficient(p3, p4);
    auto vector = Coefficient(p1, p2);
    ld DET = vector.a * line.b - line.a * vector.b;
    ld DETx = -vector.c * line.b - -line.c * vector.b;
    ld DETy = vector.a * -line.c - line.a * -vector.c;
    point P;
    P.x = DETx / DET;
    P.y = DETy / DET;
    return dist(P, p3);
}

ld Point_to_vector(point c, point a, point b) {
    if (angle(a, b, c) < 0 || angle(b, a, c) < 0) {
        return min(dist(c, a), dist(c, b));
    } else {
        return point_to_vector(a, b, c);
    }
}

bool is_intersect(point a, point b, point c, point d) {
    // c-d ? a-b
    /* point
     */ 
    auto p = Vector(d, c);
    auto v1 = Vector(d, a);
    auto v2 = Vector(d, b);
    auto vec1 = v1 * p;
    auto vec2 = v2 * p;
    if (!((vec1 < 0 && vec2 < 0) || (vec1 > 0 && vec2 > 0))) {
        return true;
    } else {
        return false;
    }
}

ld area(vector<point> &fig) {
    ld res = 0;
    for (size_t i = 0; i < fig.size(); i++) {
        point a;
        if (i == 0) {
            a = fig.back();
        } else {
            a = fig[i - 1];
        }
        point b = fig[i];
        res += Vector(a) * Vector(b);
    }
    return abs(res) / 2;
}

istream& operator>>(istream& is, point& p) {
      is >> p.x >> p.y;
      return is;
}

ostream& operator<<(ostream& os, point& p) {
      os << p.x << " " << p.y;
      return os;
}

ld segment(ld r, point goat, point p1, point p2) {
    return M_PI * r * r * angle(goat, p1, p2) / (M_PI * 2);
}

ld lepestok(ld r, point goat, point p1, point p2) {
    auto va = Vector(p1, goat);
    auto vb = Vector(p2, goat);
    return segment(r, goat, p1, p2) - abs(0.5 * (va * vb));
}

bool cmp_x(point a, point b) {
	return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool cmp_y(point a, point b) {
	return (a.y < b.y);
}

vector<point> points;
vector<point> hull;

point find_low() {
    point low = points[0];
    for (size_t i = 1; i < points.size(); i++) {
        low = min(low, points[i]);
    }
    return low;
}

bool is_turned(point a, point b, point c) {
    return (Vector(a, b) * Vector(b, c) > 0);
}

void convex_hull() {
    point low = find_low();
    points.erase(points.begin() + low.id);
    std::sort(points.begin(), points.end(), [low] (point a, point b) {
    return (((a - low) * (b - low)) > 0) ||
           (((a - low) * (b - low) == 0) && ((a - low).len() < (b - low).len()));
    });
    hull = {low, points[0]};
    for (size_t i = 1; i < points.size(); i++) {
        while (hull.size() >= 2 && !is_turned(hull[hull.size() - 2], hull[hull.size() - 1], points[i])) {
            hull.pop_back();
        }
        hull.push_back(points[i]);
    }
}
	
point top(int a, int r, int angle) {
    point p;
    p.x = r * cos((2 * M_PI * a + angle) / 5);
    p.y = r * sin((2 * M_PI * a + angle) / 5);
    return p;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout << setprecision(11) << fixed;
    ll n = 5, r = 5, ox = 10, oy = 0, ax = 0, ay = 10;
    r = sqrt(10 * 10 * 2);

    vector<point> v;

    for (int i = 0; i < 5; i++) {
        v.push_back(top(i, r, 45));
        v[i].x += ox;
        v[i].y += oy;
    }

    Vector(v[0], v[3]);

    Vector(v[1], v[4]);

    for (auto i : v) {
        cout << i << "\n";
    }


    
    return 0;
}
