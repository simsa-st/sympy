from sympy import symbols, LeviCivita, KroneckerDelta, Dummy
from sympy.physics.secondquant import evaluate_deltas, F

x, y = symbols('x,y')

def test_levicivita():
    assert LeviCivita(1, 2, 3) == 1
    assert LeviCivita(1, 3, 2) == -1
    assert LeviCivita(1, 2, 2) == 0
    i,j,k = symbols('i j k')
    assert LeviCivita(i, j, k) == LeviCivita(i,j,k, evaluate=False)
    assert LeviCivita(i, j, i) == 0
    assert LeviCivita(1, i, i) == 0
    assert LeviCivita(i, j, k).doit() == (j - i)*(k - i)*(k - j)/2
    assert LeviCivita(1, 2, 3, 1) == 0
    assert LeviCivita(4, 5, 1, 2, 3) == 1
    assert LeviCivita(4, 5, 2, 1, 3) == -1

def test_kronecker_delta():
    i, j, k = symbols('i,j,k')
    D = KroneckerDelta
    assert D(1, 1) == 1
    assert D(1, 2) == 0
    assert D(x, x) == 1
    assert D(x**2-y**2, x**2-y**2) == 1
    assert D(i, i) == 1
    assert D(i, i + 1) == 0
    assert D(0, 0) == 1
    assert D(0, 1) == 0
    # assert D(i, i + k) == D(0, k)
    assert D(i + k, i + k) == 1
    assert D(i + k, i + 1 + k) == 0
    assert D(i, j).subs(dict(i=1, j=0)) == 0
    assert D(i, j).subs(dict(i=3, j=3)) == 1


    i,j,k,l = symbols('i j k l',below_fermi=True,cls=Dummy)
    a,b,c,d = symbols('a b c d',above_fermi=True, cls=Dummy)
    p,q,r,s = symbols('p q r s',cls=Dummy)

    assert D(i,a) == 0

    assert D(i,j).is_above_fermi == False
    assert D(a,b).is_above_fermi == True
    assert D(p,q).is_above_fermi == True
    assert D(i,q).is_above_fermi == False
    assert D(a,q).is_above_fermi == True

    assert D(i,j).is_below_fermi == True
    assert D(a,b).is_below_fermi == False
    assert D(p,q).is_below_fermi == True
    assert D(p,j).is_below_fermi == True
    assert D(q,b).is_below_fermi == False

    assert not D(i,q).indices_contain_equal_information
    assert not D(a,q).indices_contain_equal_information
    assert D(p,q).indices_contain_equal_information
    assert D(a,b).indices_contain_equal_information
    assert D(i,j).indices_contain_equal_information

    assert D(q,b).preferred_index == b
    assert D(q,b).killable_index == q
    assert D(q,i).preferred_index == i
    assert D(q,i).killable_index == q
    assert D(q,p).preferred_index == p
    assert D(q,p).killable_index == q


    EV = evaluate_deltas
    assert EV(D(a,q)*F(q)) == F(a)
    assert EV(D(i,q)*F(q)) == F(i)
    assert EV(D(a,q)*F(a)) == D(a,q)*F(a)
    assert EV(D(i,q)*F(i)) == D(i,q)*F(i)
    assert EV(D(a,b)*F(a)) == F(b)
    assert EV(D(a,b)*F(b)) == F(a)
    assert EV(D(i,j)*F(i)) == F(j)
    assert EV(D(i,j)*F(j)) == F(i)
    assert EV(D(p,q)*F(q)) == F(p)
    assert EV(D(p,q)*F(p)) == F(q)
    assert EV(D(p,j)*D(p,i)*F(i)) == F(j)
    assert EV(D(p,j)*D(p,i)*F(j)) == F(i)
    assert EV(D(p,q)*D(p,i))*F(i) == D(q,i)*F(i)
