
subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)
    
    use qinit_module, only: qinit_type,add_perturbation
    use geoclaw_module, only: sea_level, grav
    use starting_module, only: tstart, mx_starting_radial, &
                           x_radial,eta_radial,u_radial
    
    implicit none
    
    ! Subroutine arguments
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
    
    ! Locals
    integer :: i,j,m
    real(kind=8) :: x0,y0,x,y,dx0,dy0,dsigma,r,Rearth,pi,eta,hU
    real(kind=8) :: a1,a2,u,xx,yy,beta
    integer :: k


    Rearth = 6367.5d3
    pi = 4.d0*atan(1.d0)
    
    ! Set flat state based on sea_level
    q = 0.d0
    forall(i=1:mx, j=1:my)
        q(1,i,j) = max(0.d0, sea_level - aux(1,i,j))
    end forall

    !write(6,*) '+++ mx_starting_radial = ', mx_starting_radial
    !write(6,*) '+++ x_radial(mx_starting_radial) = ',x_radial(mx_starting_radial)
    !write(57,*) '+++ qinit:'

    x0 = -126.d0 * pi/180.d0
    y0 = 46.9d0 * pi/180.d0

    do i=1,mx
      x = (xlower + (i-0.5d0)*dx) * pi/180.d0
      dx0 = x - x0
      do j=1,my
          if (q(1,i,j) > 0.d0) then
              y = (ylower + (j-0.5d0)*dy) * pi/180.d0
              dy0 = y - y0
              dsigma = 2.d0 * asin(sqrt(sin(0.5d0*dy0)**2 + cos(y0) * cos(y) &
                        * sin(0.5*dx0)**2))
              r = Rearth * dsigma
              eta = 0.d0
              u = 0.d0

              if (r < x_radial(mx_starting_radial-1)) then
                   k = 2
                   eta = 0.d0
                   do while ((r>x_radial(k)) .and. (k<mx_starting_radial))
                      k = k+1
                      enddo
                   !write(57,*) dx0*180.d0/pi, dy0*180.d0/pi, dsigma,r,k
                   a1 = (x_radial(k) - r)/(x_radial(k) - x_radial(k-1))
                   a2 = (r - x_radial(k-1))/(x_radial(k) - x_radial(k-1))
                   eta = a1*eta_radial(k-1) + a2*eta_radial(k)
                   u = a1*u_radial(k-1) + a2*u_radial(k)
                   if (r > 35d3) then
                       ! damp to zero
                       eta = eta * exp(-(r-35d3)/5d3)
                       u = u * exp(-(r-35d3)/5d3)
                       endif
                   !write(6,*) '+++ x,y,r: ',x,y,r
                   !write(6,*) '+++ eta = ',eta
                   q(1,i,j) = q(1,i,j) + eta
                   endif
            
              ! using u from input is probably never good,
              ! could possibly compute radial velocity from input and 
              ! phase velocity relation with water depth? 
              !hU = q(1,i,j) * u                 ! from input file

              hU = sqrt(grav*q(1,i,j)) * eta     ! from SWE eigenvector

              yy = sin(dx0)*cos(y) 
              xx = cos(y0)*sin(y) - sin(y0)*cos(y)*cos(dx0)
              beta = atan2(yy,xx)
              if (beta < 0) then
                  ! not really needed since sin,cos are 2*pi periodic
                  beta = beta + 2.d0*pi
              endif

              ! beta is bearing from (x0,y0) to (x,y), relative to North
              q(2,i,j) = hU * sin(beta)
              q(3,i,j) = hU * cos(beta)

              endif
          enddo
       enddo

    
end subroutine qinit
