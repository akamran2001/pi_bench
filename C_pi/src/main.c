#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double calc_pi(int n)
{
    double pi_4 = 1.0;
    double denom = 3.0;
    double op = -1.0;
    for (int i = 0; i < n; i++)
    {
        pi_4 += op * (1.0 / denom);
        op *= -1.0;
        denom += 2.0;
    }
    return pi_4 * 4.0;
}
int main(int argc, char *argv[])
{
    if (argc == 2)
    {
        int n = atoi(argv[1]);
        float startTime = (float)clock() / CLOCKS_PER_SEC;
        double pi = calc_pi(n);
        float endTime = (float)clock() / CLOCKS_PER_SEC;
        float timeElapsed = endTime - startTime;
        printf("Pi using %d additions is %f and took %f seconds in C", n, pi, timeElapsed);
    }
    else
    {
        printf("Please supply arguments\n");
    }
    return EXIT_SUCCESS;
}