from fastapi import APIRouter, HTTPException, status

from loguru import logger

from ._schemas import AddUser, AddUserResponse, UserResponse, HTTPError
from src.services.users import users_service


router = APIRouter()


@router.post(
    '/add_user',
    description='Add user with telegram user id, wallet address and referral id',
    responses={
        status.HTTP_201_CREATED: {
            'model': AddUserResponse,
            'description': 'User added successfully'
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': AddUserResponse,
            'description': 'Some error occured while adding new user'
        }
    }
)
async def add_user(user: AddUser):
    try:
        await users_service.add_user(user)
    except Exception as e:
        detail = f'While adding new user error occured: {e}'
        logger.error(detail)
        return AddUserResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
    else:
        return AddUserResponse(
            status=status.HTTP_201_CREATED,
            detail='OK'
        )


@router.get(
    '/{user_id}',
    description='Get user by telegram user id',
    responses={
        status.HTTP_200_OK: {
            'model': UserResponse,
            'description': 'Ok Response'
        },
        status.HTTP_404_NOT_FOUND: {
            'model': HTTPError,
            'description': 'Error Response'
        }
    }
)
async def get_user(user_id: int):
    logger.success(f'GetUser: {user_id}')
    try:
        user = await users_service.get_user(user_id=user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=f'User {user_id} not found: {e}')

    return UserResponse(
        id=user_id,
        address=user.address,
        balance=user.balance,
        contract=user.contract,
        claim_status=user.claim_status,
        time_to_claim=user.time_to_claim,
        refs=user.refs,
        daily_claim=user.daily_claim,
        boost=user.boost
    )
