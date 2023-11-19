
subroutine setprob

    !> Copy this file to your directory and modify to set up problem
    !! parameters or read other data.

    !! This version reads starting.data providing 1d profile of radially
    !! symmetric wave at time tstart

    use amr_module
    use starting_module, only: tstart, mx_starting_radial, &
         x_radial,eta_radial,u_radial
    implicit none
    integer iunit,i
    character(len=25) fname

#ifdef WHERE_AM_I
    write(*,*) 'starting setprob'
#endif

    open(unit=59, file='starting.data', status='old',form='formatted')
    read(59,*) tstart
    read(59,*) mx_starting_radial
    write(6,*) 'Reading starting.data at tstart = ',tstart

    do i=1,mx_starting_radial
        read(59,*) x_radial(i),eta_radial(i),u_radial(i)
        enddo
    close(unit=59)
              
#ifdef WHERE_AM_I
    write(*,*) 'ending   setprob'
#endif

    
end subroutine setprob
