---

title:  "Stencil 3D r3 star constant isotropic double BroadwellEP_E5-2697_CoD"

dimension    : "3D"
radius       : "r3"
weighting    : "isotropic"
kind         : "star"
coefficients : "constant"
datatype     : "double"
machine      : "BroadwellEP_E5-2697_CoD"
flavor       : "Cluster on Die"
compile_flags: "icc -O3 -xCORE-AVX2 -fno-alias -qopenmp -qopenmp -DLIKWID_PERFMON -Ilikwid-4.3.3/include -Llikwid-4.3.3/lib -Iheaders/dummy.c stencil_compilable.c -o stencil -llikwid"
flop         : "22"
scaling      : [ "900" ]
blocking     : [ "L2-3D", "L3-3D" ]
---

{%- capture basename -%}
{{page.dimension}}-{{page.radius}}-{{page.weighting}}-{{page.kind}}-{{page.coefficients}}-{{page.datatype}}-{{page.machine}}
{%- endcapture -%}

{%- capture source_code -%}
double a[M][N][P];
double b[M][N][P];
double c0;
double c1;
double c2;
double c3;

for(long k=3; k < M-3; ++k){
for(long j=3; j < N-3; ++j){
for(long i=3; i < P-3; ++i){
b[k][j][i] = c0 * a[k][j][i]
+ c1 * ((a[k][j][i-1] + a[k][j][i+1]) + (a[k-1][j][i] + a[k+1][j][i]) + (a[k][j-1][i] + a[k][j+1][i]))
+ c2 * ((a[k][j][i-2] + a[k][j][i+2]) + (a[k-2][j][i] + a[k+2][j][i]) + (a[k][j-2][i] + a[k][j+2][i]))
+ c3 * ((a[k][j][i-3] + a[k][j][i+3]) + (a[k-3][j][i] + a[k+3][j][i]) + (a[k][j-3][i] + a[k][j+3][i]))
;
}
}
}
{%- endcapture -%}
{%- capture source_code_asm -%}
vmovupd ymm11, ymmword ptr [rbx+rdi*8+0x10]
vmovupd ymm1, ymmword ptr [rbx+rdi*8+0x8]
vmovupd ymm2, ymmword ptr [rbx+rdi*8]
vaddpd ymm12, ymm11, ymmword ptr [rbx+rdi*8+0x20]
vaddpd ymm1, ymm1, ymmword ptr [rbx+rdi*8+0x28]
vaddpd ymm2, ymm2, ymmword ptr [rbx+rdi*8+0x30]
vaddpd ymm11, ymm1, ymmword ptr [r13+rdi*8+0x18]
mov rcx, qword ptr [rsp+0x1a8]
vaddpd ymm13, ymm12, ymmword ptr [rcx+rdi*8+0x18]
vaddpd ymm12, ymm11, ymmword ptr [r12+rdi*8+0x18]
mov rcx, qword ptr [rsp+0x1a0]
vaddpd ymm14, ymm13, ymmword ptr [rcx+rdi*8+0x18]
vaddpd ymm13, ymm12, ymmword ptr [r11+rdi*8+0x18]
vaddpd ymm15, ymm14, ymmword ptr [rsi+rdi*8+0x18]
vaddpd ymm14, ymm13, ymmword ptr [rdx+rdi*8+0x18]
vaddpd ymm0, ymm15, ymmword ptr [r8+rdi*8+0x18]
vaddpd ymm15, ymm2, ymmword ptr [r10+rdi*8+0x18]
vmulpd ymm0, ymm5, ymm0
vaddpd ymm1, ymm15, ymmword ptr [r14+rdi*8+0x18]
vfmadd231pd ymm0, ymm6, ymmword ptr [rbx+rdi*8+0x18]
vaddpd ymm2, ymm1, ymmword ptr [r9+rdi*8+0x18]
vfmadd231pd ymm0, ymm14, ymm4
vaddpd ymm11, ymm2, ymmword ptr [r15+rdi*8+0x18]
vfmadd231pd ymm0, ymm11, ymm3
vmovupd ymmword ptr [rax+rdi*8+0x18], ymm0
add rdi, 0x4
cmp rdi, qword ptr [rsp+0x178]
jb 0xffffffffffffff56
{%- endcapture -%}

{%- capture layercondition -%}
L1: unconditionally fulfilled
L2: unconditionally fulfilled
L3: unconditionally fulfilled
L1: P <= 2048/7;P ~ 290
L2: P <= 16384/7;P ~ 2340
L3: P <= 1441792/7;P ~ 205970
L1: 48*N*P + 16*P*(N - 3) + 48*P <= 32768;N*P ~ 10²
L2: 48*N*P + 16*P*(N - 3) + 48*P <= 262144;N*P ~ 60²
L3: 48*N*P + 16*P*(N - 3) + 48*P <= 23068672;N*P ~ 510²
{%- endcapture -%}
{%- capture iaca -%}

Throughput Analysis Report
--------------------------
Block Throughput: 15.00 Cycles       Throughput Bottleneck: Backend
Loop Count:  22
Port Binding In Cycles Per Iteration:
--------------------------------------------------------------------------------------------------
|  Port  |   0   -  DV   |   1   |   2   -  D    |   3   -  D    |   4   |   5   |   6   |   7   |
--------------------------------------------------------------------------------------------------
| Cycles |  4.0     0.0  | 15.0  | 11.5    11.1  | 11.5    10.9  |  1.0  |  1.0  |  1.0  |  0.0  |
--------------------------------------------------------------------------------------------------

DV - Divider pipe (on port 0)
D - Data fetch pipe (on ports 2 and 3)
F - Macro Fusion with the previous instruction occurred
* - instruction micro-ops not bound to a port
^ - Micro Fusion occurred
# - ESP Tracking sync uop was issued
@ - SSE instruction followed an AVX256/AVX512 instruction, dozens of cycles penalty is expected
X - instruction not supported, was not accounted in Analysis

| Num Of   |                    Ports pressure in cycles                         |      |
|  Uops    |  0  - DV    |  1   |  2  -  D    |  3  -  D    |  4   |  5   |  6   |  7   |
-----------------------------------------------------------------------------------------
|   1      |             |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vmovupd ymm11, ymmword ptr [rbx+rdi*8+0x10]
|   1      |             |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vmovupd ymm1, ymmword ptr [rbx+rdi*8+0x8]
|   1      |             |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vmovupd ymm2, ymmword ptr [rbx+rdi*8]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm12, ymm11, ymmword ptr [rbx+rdi*8+0x20]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm1, ymm1, ymmword ptr [rbx+rdi*8+0x28]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm2, ymm2, ymmword ptr [rbx+rdi*8+0x30]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm11, ymm1, ymmword ptr [r13+rdi*8+0x18]
|   1      |             |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | mov rcx, qword ptr [rsp+0x1a8]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm13, ymm12, ymmword ptr [rcx+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm12, ymm11, ymmword ptr [r12+rdi*8+0x18]
|   1      |             |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | mov rcx, qword ptr [rsp+0x1a0]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm14, ymm13, ymmword ptr [rcx+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm13, ymm12, ymmword ptr [r11+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm15, ymm14, ymmword ptr [rsi+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm14, ymm13, ymmword ptr [rdx+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm0, ymm15, ymmword ptr [r8+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm15, ymm2, ymmword ptr [r10+rdi*8+0x18]
|   1      | 1.0         |      |             |             |      |      |      |      | vmulpd ymm0, ymm5, ymm0
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm1, ymm15, ymmword ptr [r14+rdi*8+0x18]
|   2      | 1.0         |      | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vfmadd231pd ymm0, ymm6, ymmword ptr [rbx+rdi*8+0x18]
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm2, ymm1, ymmword ptr [r9+rdi*8+0x18]
|   1      | 1.0         |      |             |             |      |      |      |      | vfmadd231pd ymm0, ymm14, ymm4
|   2      |             | 1.0  | 0.5     0.5 | 0.5     0.5 |      |      |      |      | vaddpd ymm11, ymm2, ymmword ptr [r15+rdi*8+0x18]
|   1      | 1.0         |      |             |             |      |      |      |      | vfmadd231pd ymm0, ymm11, ymm3
|   2      |             |      | 0.5         | 0.5         | 1.0  |      |      |      | vmovupd ymmword ptr [rax+rdi*8+0x18], ymm0
|   1      |             |      |             |             |      |      | 1.0  |      | add rdi, 0x4
|   2^     |             |      | 0.5     0.5 | 0.5     0.5 |      | 1.0  |      |      | cmp rdi, qword ptr [rsp+0x178]
|   0*F    |             |      |             |             |      |      |      |      | jb 0xffffffffffffff56
Total Num Of Uops: 45
Analysis Notes:
Backend allocation was stalled due to unavailable allocation resources.

{%- endcapture -%}
{%- capture hostinfo -%}

################################################################################
# Logged in users
################################################################################
 10:29:41 up 109 days, 18:01,  0 users,  load average: 0.07, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT

################################################################################
# CPUset
################################################################################
Domain N:
	0,36,1,37,2,38,3,39,4,40,5,41,6,42,7,43,8,44,9,45,10,46,11,47,12,48,13,49,14,50,15,51,16,52,17,53,18,54,19,55,20,56,21,57,22,58,23,59,24,60,25,61,26,62,27,63,28,64,29,65,30,66,31,67,32,68,33,69,34,70,35,71

Domain S0:
	0,36,1,37,2,38,3,39,4,40,5,41,6,42,7,43,8,44,9,45,10,46,11,47,12,48,13,49,14,50,15,51,16,52,17,53

Domain S1:
	18,54,19,55,20,56,21,57,22,58,23,59,24,60,25,61,26,62,27,63,28,64,29,65,30,66,31,67,32,68,33,69,34,70,35,71

Domain C0:
	0,36,1,37,2,38,3,39,4,40,5,41,6,42,7,43,8,44

Domain C1:
	9,45,10,46,11,47,12,48,13,49,14,50,15,51,16,52,17,53

Domain C2:
	18,54,19,55,20,56,21,57,22,58,23,59,24,60,25,61,26,62

Domain C3:
	27,63,28,64,29,65,30,66,31,67,32,68,33,69,34,70,35,71

Domain M0:
	0,36,1,37,2,38,3,39,4,40,5,41,6,42,7,43,8,44

Domain M1:
	9,45,10,46,11,47,12,48,13,49,14,50,15,51,16,52,17,53

Domain M2:
	18,54,19,55,20,56,21,57,22,58,23,59,24,60,25,61,26,62

Domain M3:
	27,63,28,64,29,65,30,66,31,67,32,68,33,69,34,70,35,71


################################################################################
# CGroups
################################################################################
Allowed CPUs: 0-71
Allowed Memory controllers: 0-3

################################################################################
# Topology
################################################################################
--------------------------------------------------------------------------------
CPU name:	Intel(R) Xeon(R) CPU E5-2697 v4 @ 2.30GHz
CPU type:	Intel Xeon Broadwell EN/EP/EX processor
CPU stepping:	1
********************************************************************************
Hardware Thread Topology
********************************************************************************
Sockets:		2
Cores per socket:	18
Threads per core:	2
--------------------------------------------------------------------------------
HWThread	Thread		Core		Socket		Available
0		0		0		0		*
1		0		1		0		*
2		0		2		0		*
3		0		3		0		*
4		0		4		0		*
5		0		5		0		*
6		0		6		0		*
7		0		7		0		*
8		0		8		0		*
9		0		9		0		*
10		0		10		0		*
11		0		11		0		*
12		0		12		0		*
13		0		13		0		*
14		0		14		0		*
15		0		15		0		*
16		0		16		0		*
17		0		17		0		*
18		0		18		1		*
19		0		19		1		*
20		0		20		1		*
21		0		21		1		*
22		0		22		1		*
23		0		23		1		*
24		0		24		1		*
25		0		25		1		*
26		0		26		1		*
27		0		27		1		*
28		0		28		1		*
29		0		29		1		*
30		0		30		1		*
31		0		31		1		*
32		0		32		1		*
33		0		33		1		*
34		0		34		1		*
35		0		35		1		*
36		1		0		0		*
37		1		1		0		*
38		1		2		0		*
39		1		3		0		*
40		1		4		0		*
41		1		5		0		*
42		1		6		0		*
43		1		7		0		*
44		1		8		0		*
45		1		9		0		*
46		1		10		0		*
47		1		11		0		*
48		1		12		0		*
49		1		13		0		*
50		1		14		0		*
51		1		15		0		*
52		1		16		0		*
53		1		17		0		*
54		1		18		1		*
55		1		19		1		*
56		1		20		1		*
57		1		21		1		*
58		1		22		1		*
59		1		23		1		*
60		1		24		1		*
61		1		25		1		*
62		1		26		1		*
63		1		27		1		*
64		1		28		1		*
65		1		29		1		*
66		1		30		1		*
67		1		31		1		*
68		1		32		1		*
69		1		33		1		*
70		1		34		1		*
71		1		35		1		*
--------------------------------------------------------------------------------
Socket 0:		( 0 36 1 37 2 38 3 39 4 40 5 41 6 42 7 43 8 44 9 45 10 46 11 47 12 48 13 49 14 50 15 51 16 52 17 53 )
Socket 1:		( 18 54 19 55 20 56 21 57 22 58 23 59 24 60 25 61 26 62 27 63 28 64 29 65 30 66 31 67 32 68 33 69 34 70 35 71 )
--------------------------------------------------------------------------------
********************************************************************************
Cache Topology
********************************************************************************
Level:			1
Size:			32 kB
Cache groups:		( 0 36 ) ( 1 37 ) ( 2 38 ) ( 3 39 ) ( 4 40 ) ( 5 41 ) ( 6 42 ) ( 7 43 ) ( 8 44 ) ( 9 45 ) ( 10 46 ) ( 11 47 ) ( 12 48 ) ( 13 49 ) ( 14 50 ) ( 15 51 ) ( 16 52 ) ( 17 53 ) ( 18 54 ) ( 19 55 ) ( 20 56 ) ( 21 57 ) ( 22 58 ) ( 23 59 ) ( 24 60 ) ( 25 61 ) ( 26 62 ) ( 27 63 ) ( 28 64 ) ( 29 65 ) ( 30 66 ) ( 31 67 ) ( 32 68 ) ( 33 69 ) ( 34 70 ) ( 35 71 )
--------------------------------------------------------------------------------
Level:			2
Size:			256 kB
Cache groups:		( 0 36 ) ( 1 37 ) ( 2 38 ) ( 3 39 ) ( 4 40 ) ( 5 41 ) ( 6 42 ) ( 7 43 ) ( 8 44 ) ( 9 45 ) ( 10 46 ) ( 11 47 ) ( 12 48 ) ( 13 49 ) ( 14 50 ) ( 15 51 ) ( 16 52 ) ( 17 53 ) ( 18 54 ) ( 19 55 ) ( 20 56 ) ( 21 57 ) ( 22 58 ) ( 23 59 ) ( 24 60 ) ( 25 61 ) ( 26 62 ) ( 27 63 ) ( 28 64 ) ( 29 65 ) ( 30 66 ) ( 31 67 ) ( 32 68 ) ( 33 69 ) ( 34 70 ) ( 35 71 )
--------------------------------------------------------------------------------
Level:			3
Size:			22 MB
Cache groups:		( 0 36 1 37 2 38 3 39 4 40 5 41 6 42 7 43 8 44 ) ( 9 45 10 46 11 47 12 48 13 49 14 50 15 51 16 52 17 53 ) ( 18 54 19 55 20 56 21 57 22 58 23 59 24 60 25 61 26 62 ) ( 27 63 28 64 29 65 30 66 31 67 32 68 33 69 34 70 35 71 )
--------------------------------------------------------------------------------
********************************************************************************
NUMA Topology
********************************************************************************
NUMA domains:		4
--------------------------------------------------------------------------------
Domain:			0
Processors:		( 0 36 1 37 2 38 3 39 4 40 5 41 6 42 7 43 8 44 )
Distances:		10 21 31 31
Free memory:		31482.8 MB
Total memory:		32041.7 MB
--------------------------------------------------------------------------------
Domain:			1
Processors:		( 9 45 10 46 11 47 12 48 13 49 14 50 15 51 16 52 17 53 )
Distances:		21 10 31 31
Free memory:		31997.6 MB
Total memory:		32252.6 MB
--------------------------------------------------------------------------------
Domain:			2
Processors:		( 18 54 19 55 20 56 21 57 22 58 23 59 24 60 25 61 26 62 )
Distances:		31 31 10 21
Free memory:		31891 MB
Total memory:		32252.6 MB
--------------------------------------------------------------------------------
Domain:			3
Processors:		( 27 63 28 64 29 65 30 66 31 67 32 68 33 69 34 70 35 71 )
Distances:		31 31 21 10
Free memory:		31731.1 MB
Total memory:		32251.1 MB
--------------------------------------------------------------------------------
available: 4 nodes (0-3)
node 0 cpus: 0 1 2 3 4 5 6 7 8 36 37 38 39 40 41 42 43 44
node 0 size: 32041 MB
node 0 free: 31482 MB
node 1 cpus: 9 10 11 12 13 14 15 16 17 45 46 47 48 49 50 51 52 53
node 1 size: 32252 MB
node 1 free: 31997 MB
node 2 cpus: 18 19 20 21 22 23 24 25 26 54 55 56 57 58 59 60 61 62
node 2 size: 32252 MB
node 2 free: 31900 MB
node 3 cpus: 27 28 29 30 31 32 33 34 35 63 64 65 66 67 68 69 70 71
node 3 size: 32251 MB
node 3 free: 31731 MB
node distances:
node   0   1   2   3 
  0:  10  21  31  31 
  1:  21  10  31  31 
  2:  31  31  10  21 
  3:  31  31  21  10 

################################################################################
# Frequencies
################################################################################
Current CPU frequencies:
CPU 0: governor  performance min/cur/max 2.3/1.777/2.3 GHz Turbo 0
CPU 1: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 2: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 3: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 4: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 5: governor  performance min/cur/max 2.3/2.303/2.3 GHz Turbo 0
CPU 6: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 7: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 8: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 9: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 10: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 11: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 12: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 13: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 14: governor  performance min/cur/max 2.3/2.303/2.3 GHz Turbo 0
CPU 15: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 16: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 17: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 18: governor  performance min/cur/max 2.3/2.044/2.3 GHz Turbo 0
CPU 19: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 20: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 21: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 22: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 23: governor  performance min/cur/max 2.3/2.296/2.3 GHz Turbo 0
CPU 24: governor  performance min/cur/max 2.3/2.209/2.3 GHz Turbo 0
CPU 25: governor  performance min/cur/max 2.3/2.220/2.3 GHz Turbo 0
CPU 26: governor  performance min/cur/max 2.3/2.248/2.3 GHz Turbo 0
CPU 27: governor  performance min/cur/max 2.3/2.302/2.3 GHz Turbo 0
CPU 28: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 29: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 30: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 31: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 32: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 33: governor  performance min/cur/max 2.3/2.084/2.3 GHz Turbo 0
CPU 34: governor  performance min/cur/max 2.3/2.269/2.3 GHz Turbo 0
CPU 35: governor  performance min/cur/max 2.3/2.202/2.3 GHz Turbo 0
CPU 36: governor  performance min/cur/max 2.3/1.569/2.3 GHz Turbo 0
CPU 37: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 38: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 39: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 40: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 41: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 42: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 43: governor  performance min/cur/max 2.3/2.230/2.3 GHz Turbo 0
CPU 44: governor  performance min/cur/max 2.3/2.287/2.3 GHz Turbo 0
CPU 45: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 46: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 47: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 48: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 49: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 50: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 51: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 52: governor  performance min/cur/max 2.3/2.299/2.3 GHz Turbo 0
CPU 53: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 54: governor  performance min/cur/max 2.3/1.467/2.3 GHz Turbo 0
CPU 55: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 56: governor  performance min/cur/max 2.3/2.242/2.3 GHz Turbo 0
CPU 57: governor  performance min/cur/max 2.3/2.221/2.3 GHz Turbo 0
CPU 58: governor  performance min/cur/max 2.3/2.184/2.3 GHz Turbo 0
CPU 59: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 60: governor  performance min/cur/max 2.3/2.295/2.3 GHz Turbo 0
CPU 61: governor  performance min/cur/max 2.3/2.295/2.3 GHz Turbo 0
CPU 62: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 63: governor  performance min/cur/max 2.3/2.298/2.3 GHz Turbo 0
CPU 64: governor  performance min/cur/max 2.3/2.235/2.3 GHz Turbo 0
CPU 65: governor  performance min/cur/max 2.3/2.192/2.3 GHz Turbo 0
CPU 66: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 67: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 68: governor  performance min/cur/max 2.3/2.275/2.3 GHz Turbo 0
CPU 69: governor  performance min/cur/max 2.3/2.297/2.3 GHz Turbo 0
CPU 70: governor  performance min/cur/max 2.3/2.289/2.3 GHz Turbo 0
CPU 71: governor  performance min/cur/max 2.3/2.260/2.3 GHz Turbo 0

Current Uncore frequencies:
Socket 0: min/max 2.3/2.3 GHz
Socket 1: min/max 2.3/2.3 GHz

################################################################################
# Prefetchers
################################################################################
Feature               CPU 0	CPU 36	CPU 1	CPU 37	CPU 2	CPU 38	CPU 3	CPU 39	CPU 4	CPU 40	CPU 5	CPU 41	CPU 6	CPU 42	CPU 7	CPU 43	CPU 8	CPU 44	CPU 9	CPU 45	CPU 10	CPU 46	CPU 11	CPU 47	CPU 12	CPU 48	CPU 13	CPU 49	CPU 14	CPU 50	CPU 15	CPU 51	CPU 16	CPU 52	CPU 17	CPU 53	CPU 18	CPU 54	CPU 19	CPU 55	CPU 20	CPU 56	CPU 21	CPU 57	CPU 22	CPU 58	CPU 23	CPU 59	CPU 24	CPU 60	CPU 25	CPU 61	CPU 26	CPU 62	CPU 27	CPU 63	CPU 28	CPU 64	CPU 29	CPU 65	CPU 30	CPU 66	CPU 31	CPU 67	CPU 32	CPU 68	CPU 33	CPU 69	CPU 34	CPU 70	CPU 35	CPU 71	
HW_PREFETCHER         on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
CL_PREFETCHER         on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
DCU_PREFETCHER        on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
IP_PREFETCHER         on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
FAST_STRINGS          on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
THERMAL_CONTROL       on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
PERF_MON              on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
FERR_MULTIPLEX        off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
BRANCH_TRACE_STORAGE  on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
XTPR_MESSAGE          off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
PEBS                  on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
SPEEDSTEP             on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
MONITOR               on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
SPEEDSTEP_LOCK        off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
CPUID_MAX_VAL         off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
XD_BIT                on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	on	
DYN_ACCEL             off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
TURBO_MODE            off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	
TM2                   off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	off	

################################################################################
# Load
################################################################################
0.15 0.03 0.01 1/773 5021

################################################################################
# Performance energy bias
################################################################################
Performance energy bias: 7 (0=highest performance, 15 = lowest energy)

################################################################################
# NUMA balancing
################################################################################
Enabled: 1

################################################################################
# General memory info
################################################################################
MemTotal:       131889148 kB
MemFree:        130153152 kB
MemAvailable:   129856984 kB
Buffers:            9292 kB
Cached:           178160 kB
SwapCached:         6256 kB
Active:            52984 kB
Inactive:         163060 kB
Active(anon):      22288 kB
Inactive(anon):     6664 kB
Active(file):      30696 kB
Inactive(file):   156396 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:      67043324 kB
SwapFree:       67001596 kB
Dirty:              1520 kB
Writeback:             0 kB
AnonPages:         24228 kB
Mapped:           146764 kB
Shmem:               348 kB
Slab:             707552 kB
SReclaimable:     291432 kB
SUnreclaim:       416120 kB
KernelStack:       13536 kB
PageTables:         4132 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    132987896 kB
Committed_AS:     352848 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:      6144 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:      918272 kB
DirectMap2M:    46139392 kB
DirectMap1G:    89128960 kB

################################################################################
# Transparent huge pages
################################################################################
Enabled: [always] madvise never
Use zero page: 1

################################################################################
# Hardware power limits
################################################################################
RAPL domain package-1
- Limit0 long_term MaxPower 145000000uW Limit 145000000uW TimeWindow 999424us
- Limit1 short_term MaxPower 290000000uW Limit 174000000uW TimeWindow 7808us
RAPL domain dram
- Limit0 long_term MaxPower 42750000uW Limit 0uW TimeWindow 976us
RAPL domain package-0
- Limit0 long_term MaxPower 145000000uW Limit 145000000uW TimeWindow 999424us
- Limit1 short_term MaxPower 290000000uW Limit 174000000uW TimeWindow 7808us
RAPL domain dram
- Limit0 long_term MaxPower 42750000uW Limit 0uW TimeWindow 976us

################################################################################
# Modules
################################################################################

################################################################################
# Compiler
################################################################################
icc (ICC) 19.0.2.187 20190117
Copyright (C) 1985-2019 Intel Corporation.  All rights reserved.


################################################################################
# MPI
################################################################################
Intel(R) MPI Library for Linux* OS, Version 2019 Update 2 Build 20190123 (id: e2d820d49)
Copyright 2003-2019, Intel Corporation.

################################################################################
# Operating System
################################################################################
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=18.04
DISTRIB_CODENAME=bionic
DISTRIB_DESCRIPTION="Ubuntu 18.04.2 LTS"
NAME="Ubuntu"
VERSION="18.04.2 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.2 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic

################################################################################
# Operating System (LSB)
################################################################################
No LSB modules are available.

################################################################################
# Operating System Kernel
################################################################################
Linux broadep2 4.15.0-42-generic #45-Ubuntu SMP Thu Nov 15 19:32:57 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

################################################################################
# Hostname
################################################################################
broadep2.rrze.uni-erlangen.de
{%- endcapture -%}

{% include stencil_template.md %}
